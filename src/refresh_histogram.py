"""Slider callback helpers for rebuilding histogram and bucket details."""

from __future__ import annotations

import numpy as np
from matplotlib.figure import Figure

from bucket_details import BucketDetailsTable, build_bucket_outputs


RefreshHistogramResult = tuple[Figure | None, BucketDetailsTable]


def refresh_histogram(
    bucket_count: int,
    rgb_image: np.ndarray | None,
) -> RefreshHistogramResult:
    """Recompute the histogram after the user changes the bucket slider.

    Args:
        bucket_count: Updated number of hue buckets selected in the UI.
        rgb_image: Cached RGB image from the Gradio state, or `None` before upload.

    Returns:
        The refreshed histogram figure plus the reset bucket-detail rows.
    """

    if rgb_image is None:
        return None, []
    return build_bucket_outputs(int(bucket_count), np.array(rgb_image))
