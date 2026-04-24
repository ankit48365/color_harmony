"""Upload callback helpers for initializing the color bucket interface."""

from __future__ import annotations

from typing import Any

import gradio as gr
import numpy as np
from matplotlib.figure import Figure
from PIL import Image, ImageOps

from bucket_details import BucketDetailsTable, build_bucket_outputs

ComponentUpdate = dict[str, Any]
LoadImageResult = tuple[
    np.ndarray | None,
    np.ndarray | None,
    Figure | None,
    BucketDetailsTable,
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
        bucket-detail rows, upload-panel visibility update, and results-section
        visibility update.
    """

    if not file_path:
        return (
            None,
            None,
            None,
            [],
            gr.update(visible=True),
            gr.update(visible=False),
        )

    with Image.open(file_path) as uploaded_image:
        rgb_image = np.array(ImageOps.exif_transpose(uploaded_image).convert("RGB"))

    histogram, bucket_details = build_bucket_outputs(int(bucket_count), rgb_image)
    return (
        rgb_image,
        rgb_image,
        histogram,
        bucket_details,
        gr.update(visible=False),
        gr.update(visible=True),
    )
