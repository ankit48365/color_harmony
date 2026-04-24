from __future__ import annotations

from gradio_app import SECTION_CSS, create_demo


def main() -> None:
    """Launch the Gradio application.

    Args:
        None.

    Returns:
        None. Starts the Gradio server for the hue-bucket explorer.
    """

    create_demo().launch(css=SECTION_CSS)
