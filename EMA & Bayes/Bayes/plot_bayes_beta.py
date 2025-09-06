#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_bayes_from_log_static.py

Static visualization of Beta distribution evolution for each key/value
from priors_log.csv.
- 2x2 subplots per page
- Keyboard left/right to change pages
- Legend on the right side of each subplot
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta
import math

# Fixed CSV file path
LOGFILE = "priors_log_bayes.csv"

# Config
PER_PAGE = 4         # subplots per page

# -------- helpers --------
def update_beta(alpha, beta_param, reward, threshold=0.5):
    """Update Beta distribution parameters with reward"""
    if reward >= threshold:
        alpha += 1
    else:
        beta_param += 1
    return alpha, beta_param


def best_grid(n):
    """Decide subplot grid (rows, cols)"""
    if n == 0:
        return 1, 1
    ncols = math.ceil(math.sqrt(n))
    nrows = math.ceil(n / ncols)
    return nrows, ncols


def plot_beta_for_key(ax, df, key):
    """Plot only the final Beta distribution for each value under this key"""
    values = df.loc[df["key"] == key, "value"].unique()
    x = np.linspace(0, 1, 500)

    cmap = plt.get_cmap("tab20")   # 20 种不同颜色
    for idx, value in enumerate(values):
        alpha, beta_param = 1, 1
        rewards = df.loc[(df["key"] == key) & (df["value"] == value), "reward"].tolist()

        # 更新所有 reward，但只保留最终结果
        for r in rewards:
            alpha, beta_param = update_beta(alpha, beta_param, r)

        # 分配颜色
        color = cmap(idx % 20)

        # 只画最后一次
        y = beta.pdf(x, alpha, beta_param)
        ax.plot(x, y, label=f"{value} (Final α={alpha}, β={beta_param})",
                color=color, linewidth=2)
        ax.fill_between(x, y, 0, alpha=0.15, color=color)

    ax.set_title(f"Key: {key}", fontsize=10)
    ax.set_xlabel("p (probability)", fontsize=8)
    ax.set_ylabel("density", fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=7, loc="upper left", bbox_to_anchor=(1.01, 1.0), frameon=False)




# -------- global states --------
page = [0]
keys = []


def draw_page(fig, df, p, total_pages):
    fig.clf()
    start = p * PER_PAGE
    end = min((p + 1) * PER_PAGE, len(keys))
    keys_page = keys[start:end]

    nrows, ncols = best_grid(len(keys_page))
    axes = fig.subplots(nrows, ncols, squeeze=False)

    for ax, key in zip(axes.flat, keys_page):
        plot_beta_for_key(ax, df, key)

    for ax in axes.flat[len(keys_page):]:
        ax.axis("off")

    fig.suptitle(f"Bayes Beta Evolution | Page {p+1}/{total_pages}", fontsize=14)
    fig.tight_layout()
    fig.canvas.draw()


def on_key(event):
    total_pages = math.ceil(len(keys) / PER_PAGE)
    if event.key == "right":
        page[0] = (page[0] + 1) % total_pages
        draw_page(fig, df, page[0], total_pages)
    elif event.key == "left":
        page[0] = (page[0] - 1) % total_pages
        draw_page(fig, df, page[0], total_pages)


# -------- main --------
if __name__ == "__main__":
    print(f"[INFO] Reading log file: {LOGFILE}")
    df = pd.read_csv(LOGFILE)
    df.columns = df.columns.str.strip().str.lower()
    if not {"key", "value", "reward"}.issubset(df.columns):
        raise ValueError("CSV must contain 'key', 'value', 'reward' columns")

    keys = sorted(df["key"].unique())
    total_pages = math.ceil(len(keys) / PER_PAGE)

    fig = plt.figure(figsize=(12, 8))
    fig.canvas.mpl_connect("key_press_event", on_key)

    draw_page(fig, df, page[0], total_pages)
    plt.show()
