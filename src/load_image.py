from __future__ import annotations

from typing import Any

import gradio as gr
import numpy as np
from matplotlib.figure import Figure
from PIL import Image, ImageOps

from build_histogram import build_histogram

ComponentUpdate = dict[str, Any]
LoadImageResult = tuple[
    np.ndarray | None,
    np.ndarray | None,
    Figure | None,
    ComponentUpdate,
    ComponentUpdate,
]


def load_image(file_path: str | None, bucket_count: int) -> LoadImageResult:
    """Load the uploaded JPG and prepare the first histogram render.

    Args:
        file_path: Filesystem path to the uploaded JPG, or `None` when no file is selected.
        bucket_count: Number of hue buckets to use for the first histogram.

    Returns:
        A tuple with the stored image state, preview image, histogram figure,
        upload-panel visibility update, and results-section visibility update.
    """

    if not file_path:
        return (
            None,
            None,
            None,
            gr.update(visible=True),
            gr.update(visible=False),
        )

    with Image.open(file_path) as uploaded_image:
        rgb_image = np.array(ImageOps.exif_transpose(uploaded_image).convert("RGB"))

    histogram = build_histogram(rgb_image, int(bucket_count))
    return (
        rgb_image,
        rgb_image,
        histogram,
        gr.update(visible=False),
        gr.update(visible=True),
    )
