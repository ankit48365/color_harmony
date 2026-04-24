from __future__ import annotations

from typing import Any

import gradio as gr

from app_config import DEFAULT_BUCKETS

ComponentUpdate = dict[str, Any]
ResetAppResult = tuple[
    None,
    None,
    None,
    None,
    int,
    ComponentUpdate,
    ComponentUpdate,
]


def reset_app() -> ResetAppResult:
    """Reset the Gradio interface back to its upload-first state.

    Args:
        None.

    Returns:
        A tuple that clears the file input, image state, preview, histogram, slider value,
        upload-panel visibility, and results-section visibility.
    """

    return (
        None,
        None,
        None,
        None,
        DEFAULT_BUCKETS,
        gr.update(visible=True),
        gr.update(visible=False),
    )
