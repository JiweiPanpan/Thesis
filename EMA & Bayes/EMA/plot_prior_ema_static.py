#!/usr/bin/env python3
"""
Create a static 2x2 page snapshot of EMA priors and save as a single image.

Usage:
    python3 plot_prior_ema_static.py --input priors_log_ema.csv --page 0 --output combined_page0.png

This adapts the interactive animation logic from `plot_prior_ema.py` and writes a single image with
up to 4 keys (one per subplot) laid out in a 2x2 grid.
"""

import argparse
import math
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import os

plt.style.use("seaborn-v0_8")

PER_PAGE = 4
# Make tick numbers and axis labels smaller for compact figures
plt.rcParams["xtick.labelsize"] = 6
plt.rcParams["ytick.labelsize"] = 6
plt.rcParams["axes.labelsize"] = 7
plt.rcParams["axes.titlesize"] = 8
plt.rcParams["legend.fontsize"] = 6


def load_data(path):
    try:
        df = pd.read_csv(path)
        df = df.reset_index().rename(columns={"index": "iteration"})
        df["new_prior"] = pd.to_numeric(df.get("new_prior", 0.0), errors="coerce")
        df["iteration"] = pd.to_numeric(df.get("iteration", 0), errors="coerce").fillna(
            0
        )
        if "mode" not in df.columns:
            df["mode"] = "ema"
        return df
    except Exception as e:
        print("Failed to load CSV:", e)
        return pd.DataFrame(columns=["iteration", "key", "value", "new_prior", "mode"])


def best_grid(n):
    if n == 0:
        return 1, 1
    ncols = math.ceil(math.sqrt(n))
    nrows = math.ceil(n / ncols)
    return nrows, ncols


def make_snapshot(
    df, page_idx=0, out_path="combined.png", figsize=(8, 6), pattern=None
):
    df = df[df["mode"] == "ema"]
    keys = sorted(df["key"].unique())
    if pattern:
        keys = [k for k in keys if pattern in str(k)]
    if len(keys) == 0:
        raise SystemExit("No keys found in CSV (mode=ema).")

    total_pages = math.ceil(len(keys) / PER_PAGE)
    page_idx = int(page_idx) % max(1, total_pages)
    start = page_idx * PER_PAGE
    end = start + PER_PAGE
    keys_page = keys[start:end]

    # Create a 2x2 layout for the 4-per-page snapshot
    # Use constrained_layout=False and manually tighten spacing to reduce white space
    fig = plt.figure(figsize=figsize, constrained_layout=False)
    # Force a 2x2 layout for readability
    nrows, ncols = 2, 2
    axes = fig.subplots(nrows, ncols, squeeze=False)

    # default max iteration from data
    max_iter = int(df["iteration"].max()) if not df.empty else 0
    # if user supplied --max-iter, prefer that as the x-axis max
    if hasattr(make_snapshot, "max_iter") and make_snapshot.max_iter is not None:
        try:
            max_iter = int(make_snapshot.max_iter)
        except Exception:
            pass
    color_map = plt.get_cmap("tab20")

    for ax, key in zip(axes.flat, keys_page):
        group = df[df["key"] == key]
        for idx, (value, g2) in enumerate(group.groupby("value")):
            base_color = color_map(idx % 20)
            # apply max_iter filter if provided by user
            if hasattr(make_snapshot, "max_iter") and make_snapshot.max_iter is not None:
                g2 = g2[g2["iteration"] <= make_snapshot.max_iter]
            y = g2["new_prior"].fillna(0.0)
            label = f"{value}"
            ax.plot(
                g2["iteration"],
                y,
                label=label,
                linewidth=1.6,
                alpha=0.9,
                color=base_color,
                linestyle="-",
            )

        ax.set_title(str(key), fontsize=8)
        ax.set_xlabel("Iteration", fontsize=7)
        ax.set_ylabel("Prior", fontsize=7)
        ax.grid(True, alpha=0.3)
        ax.set_xlim(0, max(20, max_iter + 2))
        ax.set_ylim(0.0, 1.05)
        # Keep legend inside the axes to avoid expanding the figure width
        ax.legend(fontsize=6, loc="lower right", frameon=False)

    # Turn off any unused axes
    for ax in axes.flat[len(keys_page) :]:
        ax.axis("off")

    # Smaller suptitle and tighter layout to reduce whitespace
    # fig.suptitle(f"EMA Priors | Page {page_idx+1}/{total_pages}", fontsize=10, y=0.99)
    fig.tight_layout(pad=0.2)
    # Manually adjust margins and spacing to be compact; reduce horizontal spacing between columns
    fig.subplots_adjust(
        top=0.92, hspace=0.30, wspace=0.1, left=0.05, right=0.99, bottom=0.06
    )

    # Ensure output dir exists
    outdir = os.path.dirname(out_path) or "."
    os.makedirs(outdir, exist_ok=True)
    # Save with moderate DPI; keep size compact
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    print(f"Saved snapshot to: {out_path}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--input", "-i", default="priors_log_ema.csv", help="CSV input file")
    p.add_argument("--page", "-p", default=0, type=int, help="Page index (0-based)")
    p.add_argument(
        "--output", "-o", default="combined_page.png", help="Output PNG path"
    )
    p.add_argument("--figsize", default="8,4", help="Figure size as 'w,h' (inches)")
    p.add_argument(
        "--pattern",
        "-t",
        default=None,
        help="Substring to filter keys (e.g. ComputePathToState)",
    )
    p.add_argument("--max-iter", default=None, type=int, help="Maximum iteration to plot (inclusive)")
    args = p.parse_args()

    w, h = (8, 3)
    try:
        w, h = tuple(float(x.strip()) for x in args.figsize.split(","))
    except Exception:
        pass

    df = load_data(args.input)
    if df.empty:
        print("Input CSV appears empty or failed to load. Exiting.")
        raise SystemExit(1)

    # attach max_iter to function for simple scoping
    make_snapshot.max_iter = args.max_iter
    make_snapshot(
        df,
        page_idx=args.page,
        out_path=args.output,
        figsize=(w, h),
        pattern=args.pattern,
    )
