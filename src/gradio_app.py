"""Gradio UI composition for the color harmony demo."""

from __future__ import annotations

import gradio as gr

from app_config import DEFAULT_BUCKETS
from load_image import load_image
from refresh_histogram import refresh_histogram
from reset_app import reset_app
from update_bucket_weights import update_bucket_weights

SECTION_CSS = """
:root {
    --page-bg: #f7f3e9;
    --card-bg: #fffdf7;
    --card-border: #d7cfbd;
    --ink: #1f2a33;
    --muted: #5c6570;
}

body, .gradio-container {
    background:
        radial-gradient(circle at top left, rgba(255, 217, 156, 0.45), transparent 28%),
        linear-gradient(180deg, #faf6ec 0%, #f2ede0 100%);
    color: var(--ink);
    font-family: "Trebuchet MS", "Aptos", sans-serif;
}

.hero-card,
.section-card {
    background: rgba(255, 253, 247, 0.92);
    border: 1px solid var(--card-border);
    border-radius: 18px;
    box-shadow: 0 18px 45px rgba(70, 56, 21, 0.08);
}

.hero-card {
    padding: 22px 26px 10px 26px;
    margin-bottom: 18px;
}

.hero-card .prose h1,
.hero-card .prose p,
.hero-card .prose strong,
.section-card .prose h3 {
    color: var(--ink) !important;
}

.hero-card .prose p {
    opacity: 1;
}

.hero-card .prose code {
    background: #2a3138;
    color: #fff7e5 !important;
    border-radius: 6px;
    padding: 0.15rem 0.35rem;
}

.section-card {
    padding: 14px;
}

.section-note {
    color: var(--muted);
    font-size: 0.95rem;
}
"""


def create_demo() -> gr.Blocks:
    """Create the Gradio Blocks interface for the hue-bucket explorer.

    Args:
        None.

    Returns:
        A fully wired `gr.Blocks` application with upload, slider, and histogram sections.
    """

    with gr.Blocks(title="Hue Bucket Histogram") as demo:
        image_state = gr.State(None)

        with gr.Column(elem_classes=["hero-card"]):
            gr.Markdown(
                """
                # JPG Color Bucket Explorer
                Upload a `.jpg` image, choose a value `X` from **3 to 30**, and see how
                many pixels land in each hue class.

                With `X = 3`, the buckets are centered on **red**, **green**, and **blue**.
                Larger `X` values split the hue wheel into finer color families, and each
                bucket now includes a live hex code, pixel share, and editable saturation
                weight.
                """
            )

        with gr.Group(visible=True) as upload_panel:
            upload_input = gr.File(
                label="Upload a JPG Image",
                file_types=[".jpg", ".jpeg"],
                type="filepath",
            )

        with gr.Row(visible=False) as result_sections:
            with gr.Column(elem_classes=["section-card"], scale=1):
                gr.Markdown("### Section 1: Uploaded Image")
                image_preview = gr.Image(
                    label="Image Preview",
                    interactive=False,
                    buttons=["fullscreen"],
                )
                redo_button = gr.Button("Redo / Upload New Image", variant="secondary")

            with gr.Column(elem_classes=["section-card"], scale=1):
                gr.Markdown("### Section 2: Choose X")
                bucket_slider = gr.Slider(
                    minimum=3,
                    maximum=30,
                    value=DEFAULT_BUCKETS,
                    step=1,
                    label="X (number of hue classes)",
                )
                gr.Markdown(
                    "Pixels are assigned to the nearest hue bucket center on the color wheel.",
                    elem_classes=["section-note"],
                )

            with gr.Column(elem_classes=["section-card"], scale=2):
                gr.Markdown("### Section 3: Color Histogram")
                histogram_plot = gr.Plot(label="Hue Histogram")
                gr.Markdown("### Section 4: Bucket Details")
                gr.Markdown(
                    "Each row shows the histogram label with its current hex code, "
                    "the share of total pixels, and a saturation weight. `50` is the "
                    "midpoint, `0` removes color, and `100` fully saturates the hue.",
                    elem_classes=["section-note"],
                )
                bucket_details = gr.Dataframe(
                    headers=["Color (HEX)", "Pixel Share", "Saturation Weight"],
                    datatype=["str", "str", "number"],
                    type="array",
                    interactive=True,
                    static_columns=[0, 1],
                    wrap=True,
                    max_height=420,
                    column_widths=["46%", "22%", "32%"],
                    show_row_numbers=True,
                )

        upload_input.change(  # pylint: disable=no-member
            fn=load_image,
            inputs=[upload_input, bucket_slider],
            outputs=[
                image_state,
                image_preview,
                histogram_plot,
                bucket_details,
                upload_panel,
                result_sections,
            ],
        )

        bucket_slider.change(  # pylint: disable=no-member
            fn=refresh_histogram,
            inputs=[bucket_slider, image_state],
            outputs=[histogram_plot, bucket_details],
        )

        bucket_details.edit(  # pylint: disable=no-member
            fn=update_bucket_weights,
            inputs=[bucket_details, bucket_slider, image_state],
            outputs=[histogram_plot, bucket_details],
        )

        redo_button.click(  # pylint: disable=no-member
            fn=reset_app,
            inputs=[],
            outputs=[
                upload_input,
                image_state,
                image_preview,
                histogram_plot,
                bucket_slider,
                bucket_details,
                upload_panel,
                result_sections,
            ],
        )

    return demo
