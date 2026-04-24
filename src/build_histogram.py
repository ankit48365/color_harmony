from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from compute_hue_statistics import compute_hue_statistics


def build_histogram(rgb_image: np.ndarray, bucket_count: int) -> Figure:
    """Build the hue histogram figure for the provided RGB image.

    Args:
        rgb_image: Image array shaped like `(height, width, 3)` with RGB pixel data.
        bucket_count: Number of hue buckets to visualize.

    Returns:
        A Matplotlib figure containing the styled histogram.
    """

    counts, _, tick_labels, bar_colors = compute_hue_statistics(rgb_image, bucket_count)

    fig_width = max(8.0, bucket_count * 0.45)
    fig, ax = plt.subplots(figsize=(fig_width, 4.6), dpi=120)
    fig.patch.set_facecolor("#fffdf7")
    ax.set_facecolor("#fffdf7")

    bars = ax.bar(
        np.arange(bucket_count),
        counts,
        width=0.86,
        color=bar_colors,
        edgecolor=bar_colors,
        linewidth=1.8,
    )

    for bar, color in zip(bars, bar_colors):
        bar.set_facecolor((*color, 0.22))
        bar.set_edgecolor(color)
        bar.set_hatch("////")
        bar.set_linewidth(1.8)

    ax.set_title(
        f"Pixel Counts Across {bucket_count} Hue Classes",
        fontsize=14,
        fontweight="bold",
        color="#1f2a33",
        pad=14,
    )
    ax.set_xlabel("Hue Class", fontsize=11, color="#31404d")
    ax.set_ylabel("Pixel Count", fontsize=11, color="#31404d")
    ax.set_xticks(np.arange(bucket_count))
    ax.set_xticklabels(tick_labels, rotation=45 if bucket_count > 10 else 0, ha="right")
    ax.grid(axis="y", linestyle=":", linewidth=0.9, alpha=0.35)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#9e9788")
    ax.spines["bottom"].set_color("#9e9788")
    ax.tick_params(colors="#44515c")
    ax.margins(x=0.01)
    plt.tight_layout()
    return fig
