"""Reset callback helpers for returning the UI to its initial state."""

from __future__ import annotations

from typing import Any

import gradio as gr

from app_config import DEFAULT_BUCKETS
from bucket_details import BucketDetailsTable

ComponentUpdate = dict[str, Any]
ResetAppResult = tuple[
    None,
    None,
    None,
    None,
    int,
    BucketDetailsTable,
    ComponentUpdate,
    ComponentUpdate,
]


def reset_app() -> ResetAppResult:
    """Reset the Gradio interface back to its upload-first state.

    Args:
        None.

    Returns:
        A tuple that clears the file input, image state, preview, histogram, slider
        value, bucket-detail rows, upload-panel visibility, and results-section
        visibility.
    """

    return (
        None,
        None,
        None,
        None,
        DEFAULT_BUCKETS,
        [],
        gr.update(visible=True),
        gr.update(visible=False),
    )
