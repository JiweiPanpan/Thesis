#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math

LOG_FILE = "/home/jiwei/Desktop/Thesis/EMA & Bayes/EMA/priors_log_ema.csv"
plt.style.use("seaborn-v0_8")

# -------- Configuration --------
MODE = "ema"   # Fixed to "ema"
PER_PAGE = 4   # Number of plots per page

def load_data():
    try:
        df = pd.read_csv(LOG_FILE)
        df["new_prior"] = pd.to_numeric(df.get("new_prior", 0.0), errors="coerce")

        df = df.sort_values("timestamp").reset_index(drop=True)
        df["global_iter"] = df.index

        df["iteration"] = df.groupby("key").cumcount()

        if "mode" not in df.columns:
            df["mode"] = "ema"
        return df
    except Exception as e:
        print("Error loading CSV:", e)
        return pd.DataFrame(columns=["iteration", "global_iter", "key", "value", "new_prior", "mode"])

def best_grid(n):
    """Automatically decide number of rows and columns"""
    if n == 0:
        return 1, 1
    ncols = math.ceil(math.sqrt(n))
    nrows = math.ceil(n / ncols)
    return nrows, ncols

# ------- Global states --------
page = [0]          # Current page
paused = [False]    # Pause state for animation

def animate(_frame):
    if paused[0]:
        return  # Skip refresh when paused

    df = load_data()
    if df.empty:
        return

    # Only keep EMA data
    df = df[df["mode"] == MODE]

    keys = sorted(df["key"].unique())
    n = len(keys)
    if n == 0:
        return

    # Calculate pagination
    total_pages = math.ceil(n / PER_PAGE)
    cur_page = page[0] % total_pages
    start = cur_page * PER_PAGE
    end = start + PER_PAGE
    keys_page = keys[start:end]

    fig.clf()
    nrows, ncols = best_grid(len(keys_page))
    axes = fig.subplots(nrows, ncols, squeeze=False)

    color_map = plt.get_cmap("tab20")

    for ax, key in zip(axes.flat, keys_page):
        group = df[df["key"] == key]
        max_iter = int(group["iteration"].max()) if not group.empty else 0

        for idx, (value, g2) in enumerate(group.groupby("value")):
            base_color = color_map(idx % 20)
            y = g2["new_prior"]
            label = f"{value} "
            ax.plot(
                g2["iteration"], y,
                label=label, linewidth=2, alpha=0.9,
                color=base_color, linestyle="-"  # Always solid line
            )

        ax.set_title(str(key), fontsize=10)
        ax.set_xlabel("Iteration (per key)", fontsize=8)
        ax.set_ylabel("Prior", fontsize=8)
        ax.grid(True, alpha=0.3)
        ax.set_xlim(0, max(20, max_iter + 2))
        ax.set_ylim(0.0, 1.05)
        ax.legend(fontsize=8, loc="upper left", bbox_to_anchor=(1.01, 1.0))

    for ax in axes.flat[len(keys_page):]:
        ax.axis("off")

    fig.suptitle(f"EMA Priors | Page {cur_page+1}/{total_pages}", fontsize=12)
    fig.tight_layout()

# ------- Keyboard events --------
def on_key(event):
    if event.key == "right":
        page[0] += 1   # Next page
        animate(0)
        plt.draw()
    elif event.key == "left":
        page[0] -= 1   # Previous page
        animate(0)
        plt.draw()
    elif event.key == " ":
        paused[0] = not paused[0]  # Toggle pause
        print("Paused" if paused[0] else "Resumed")

fig = plt.figure(figsize=(12, 8))
fig.canvas.mpl_connect("key_press_event", on_key)

ani = FuncAnimation(fig, animate, interval=3000, cache_frame_data=False)
plt.show()
