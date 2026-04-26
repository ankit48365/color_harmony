"""Hue bucket analysis helpers for histogram and detail views."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np
from matplotlib.colors import hsv_to_rgb, rgb_to_hsv

from hue_label import hue_label

DEFAULT_SATURATION_WEIGHT = 50
DEFAULT_BAR_SATURATION = 0.75
DEFAULT_BAR_VALUE = 0.95


@dataclass(frozen=True)
class HueStatistics:
    """Structured hue-bucket analysis results used by the UI and histogram."""

    counts: np.ndarray
    centers: np.ndarray
    tick_labels: list[str]
    bar_colors: np.ndarray
    saturation_weights: list[int]
    hsv_pixels: np.ndarray
    bucket_indices: np.ndarray


def normalize_saturation_weight(raw_weight: object) -> int:
    """Clamp a user-provided saturation weight into the supported 0-100 range."""

    if raw_weight in (None, ""):
        return DEFAULT_SATURATION_WEIGHT

    try:
        weight = int(round(float(raw_weight)))
    except (TypeError, ValueError):
        return DEFAULT_SATURATION_WEIGHT

    return max(0, min(100, weight))


def normalize_saturation_weights(
    bucket_count: int,
    saturation_weights: Sequence[object] | None = None,
) -> list[int]:
    """Build a sanitized per-bucket weight list, defaulting each bucket to 50."""

    provided_weights = list(saturation_weights or [])
    return [
        normalize_saturation_weight(
            provided_weights[index]
            if index < len(provided_weights)
            else DEFAULT_SATURATION_WEIGHT
        )
        for index in range(bucket_count)
    ]


def rgb_to_hex(color: np.ndarray) -> str:
    """Convert a normalized RGB triplet into a user-facing uppercase hex code."""

    red, green, blue = np.clip(np.rint(color * 255.0), 0, 255).astype(int)
    return f"#{red:02X}{green:02X}{blue:02X}"


def apply_saturation_weight(
    base_saturation: np.ndarray | float,
    saturation_weights: np.ndarray | Sequence[float] | float,
) -> np.ndarray:
    """Scale saturation so 50 keeps the base value, 0 removes color, and 100 maxes it."""

    base = np.asarray(base_saturation, dtype=np.float32)
    weight_scale = np.clip(np.asarray(saturation_weights, dtype=np.float32), 0.0, 100.0)
    weight_scale = weight_scale / 100.0
    midpoint = 0.5

    return np.where(
        weight_scale <= midpoint,
        base * (weight_scale / midpoint),
        base + ((weight_scale - midpoint) / midpoint) * (1.0 - base),
    ).astype(np.float32)


def analyze_hue_buckets(
    rgb_image: np.ndarray,
    bucket_count: int,
    saturation_weights: Sequence[object] | None = None,
) -> HueStatistics:
    """Compute counts, labels, and weighted bucket colors for an RGB image."""

    pixels = rgb_image.reshape(-1, 3).astype(np.float32) / 255.0
    hsv_pixels = rgb_to_hsv(pixels)
    hue_deg = hsv_pixels[:, 0] * 360.0

    step = 360.0 / bucket_count
    bucket_indices = np.floor(((hue_deg + (step / 2.0)) % 360.0) / step).astype(int)
    counts = np.bincount(bucket_indices, minlength=bucket_count)
    centers = (np.arange(bucket_count, dtype=np.float32) * step) % 360.0
    weights = normalize_saturation_weights(bucket_count, saturation_weights)
    representative_saturation = apply_saturation_weight(
        np.full(bucket_count, DEFAULT_BAR_SATURATION, dtype=np.float32),
        np.array(weights, dtype=np.float32),
    )

    bar_colors = hsv_to_rgb(
        np.column_stack(
            [
                centers / 360.0,
                representative_saturation,
                np.full(bucket_count, DEFAULT_BAR_VALUE, dtype=np.float32),
            ]
        )
    )

    tick_labels = (
        [hue_label(center) for center in centers]
        if bucket_count <= 12
        else [f"{int(round(center))} deg" for center in centers]
    )
    return HueStatistics(
        counts=counts,
        centers=centers,
        tick_labels=tick_labels,
        bar_colors=bar_colors,
        saturation_weights=weights,
        hsv_pixels=hsv_pixels,
        bucket_indices=bucket_indices,
    )


def compute_hue_statistics(
    rgb_image: np.ndarray,
    bucket_count: int,
    saturation_weights: Sequence[object] | None = None,
) -> tuple[np.ndarray, np.ndarray, list[str], np.ndarray]:
    """Compute hue-bucket counts, labels, and colors for an RGB image.

    Args:
        rgb_image: Image array shaped like `(height, width, 3)` with 8-bit RGB pixels.
        bucket_count: Number of evenly spaced hue classes to build across 360 degrees.
        saturation_weights: Optional per-bucket saturation weights in the 0-100 range.

    Returns:
        A tuple of `(counts, centers, tick_labels, bar_colors)` for the histogram view.
    """

    statistics = analyze_hue_buckets(rgb_image, bucket_count, saturation_weights)
    return (
        statistics.counts,
        statistics.centers,
        statistics.tick_labels,
        statistics.bar_colors,
    )


def compute_bucket_table_rows_from_statistics(
    statistics: HueStatistics,
) -> list[list[str | int]]:
    """Format the per-bucket rows shown in the editable Gradio table."""

    total_pixels = max(int(statistics.counts.sum()), 1)
    return [
        [
            f"{label} ({rgb_to_hex(color)})",
            f"{(count / total_pixels) * 100:.2f}%",
            weight,
        ]
        for label, count, color, weight in zip(
            statistics.tick_labels,
            statistics.counts,
            statistics.bar_colors,
            statistics.saturation_weights,
        )
    ]


def build_adjusted_preview_image(
    statistics: HueStatistics,
    image_shape: tuple[int, ...],
) -> np.ndarray:
    """Apply the bucket weights to the uploaded image while preserving each pixel's hue/value."""

    adjusted_hsv = statistics.hsv_pixels.copy()
    pixel_weights = np.array(statistics.saturation_weights, dtype=np.float32)[
        statistics.bucket_indices
    ]
    adjusted_hsv[:, 1] = apply_saturation_weight(adjusted_hsv[:, 1], pixel_weights)
    adjusted_rgb = hsv_to_rgb(adjusted_hsv).reshape(image_shape)
    return np.clip(np.rint(adjusted_rgb * 255.0), 0, 255).astype(np.uint8)
