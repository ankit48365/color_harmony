from __future__ import annotations

import numpy as np
from matplotlib.figure import Figure

from build_histogram import build_histogram


def refresh_histogram(bucket_count: int, rgb_image: np.ndarray | None) -> Figure | None:
    """Recompute the histogram after the user changes the bucket slider.

    Args:
        bucket_count: Updated number of hue buckets selected in the UI.
        rgb_image: Cached RGB image from the Gradio state, or `None` before upload.

    Returns:
        The refreshed histogram figure, or `None` when there is no uploaded image yet.
    """

    if rgb_image is None:
        return None
    return build_histogram(np.array(rgb_image), int(bucket_count))
