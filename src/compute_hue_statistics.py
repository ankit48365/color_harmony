from __future__ import annotations

import numpy as np
from matplotlib.colors import hsv_to_rgb, rgb_to_hsv

from hue_label import hue_label


def compute_hue_statistics(
    rgb_image: np.ndarray,
    bucket_count: int,
) -> tuple[np.ndarray, np.ndarray, list[str], np.ndarray]:
    """Compute hue-bucket counts, labels, and colors for an RGB image.

    Args:
        rgb_image: Image array shaped like `(height, width, 3)` with 8-bit RGB pixels.
        bucket_count: Number of evenly spaced hue classes to build across 360 degrees.

    Returns:
        A tuple of `(counts, centers, tick_labels, bar_colors)` for the histogram view.
    """

    pixels = rgb_image.reshape(-1, 3).astype(np.float32) / 255.0
    hsv_pixels = rgb_to_hsv(pixels)
    hue_deg = hsv_pixels[:, 0] * 360.0

    step = 360.0 / bucket_count
    bucket_indices = np.floor(((hue_deg + (step / 2.0)) % 360.0) / step).astype(int)
    counts = np.bincount(bucket_indices, minlength=bucket_count)
    centers = (np.arange(bucket_count, dtype=np.float32) * step) % 360.0

    bar_colors = hsv_to_rgb(
        np.column_stack(
            [
                centers / 360.0,
                np.full(bucket_count, 0.75, dtype=np.float32),
                np.full(bucket_count, 0.95, dtype=np.float32),
            ]
        )
    )

    tick_labels = (
        [hue_label(center) for center in centers]
        if bucket_count <= 12
        else [f"{int(round(center))} deg" for center in centers]
    )
    return counts, centers, tick_labels, bar_colors
