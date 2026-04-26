"""Histogram rendering helpers for the color harmony demo."""

from __future__ import annotations

from collections.abc import Sequence

# `matplotlib.use("Agg")` must be set before importing pyplot.
# pylint: disable=wrong-import-position
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from compute_hue_statistics import HueStatistics, analyze_hue_buckets


def build_histogram_from_statistics(statistics: HueStatistics) -> Figure:
    """Build the hue histogram figure from a precomputed set of bucket statistics."""

    counts = statistics.counts
    tick_labels = statistics.tick_labels
    bar_colors = statistics.bar_colors
    bucket_count = len(counts)

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

    for histogram_bar, color in zip(bars, bar_colors):
        histogram_bar.set_facecolor((*color, 0.22))
        histogram_bar.set_edgecolor(color)
        histogram_bar.set_hatch("////")
        histogram_bar.set_linewidth(1.8)

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


def build_histogram(
    rgb_image: np.ndarray,
    bucket_count: int,
    saturation_weights: Sequence[object] | None = None,
) -> Figure:
    """Build the hue histogram figure for the provided RGB image.

    Args:
        rgb_image: Image array shaped like `(height, width, 3)` with RGB pixel data.
        bucket_count: Number of hue buckets to visualize.
        saturation_weights: Optional per-bucket saturation weights in the 0-100 range.

    Returns:
        A Matplotlib figure containing the styled histogram.
    """

    statistics = analyze_hue_buckets(rgb_image, bucket_count, saturation_weights)
    return build_histogram_from_statistics(statistics)
