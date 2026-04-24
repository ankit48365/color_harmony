from __future__ import annotations

import matplotlib
import numpy as np
from PIL import Image, ImageOps

import gradio as gr

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb, rgb_to_hsv

DEFAULT_BUCKETS = 6
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

.section-card {
    padding: 14px;
}

.section-note {
    color: var(--muted);
    font-size: 0.95rem;
}
"""


def hue_label(center_deg: float) -> str:
    names = [
        "Red",
        "Orange",
        "Yellow",
        "Chartreuse",
        "Green",
        "Spring",
        "Cyan",
        "Azure",
        "Blue",
        "Violet",
        "Magenta",
        "Rose",
    ]
    index = int(((center_deg % 360.0) / 360.0) * len(names)) % len(names)
    return names[index]


def compute_hue_statistics(
    rgb_image: np.ndarray,
    bucket_count: int,
) -> tuple[np.ndarray, np.ndarray, list[str], np.ndarray]:
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


def build_histogram(rgb_image: np.ndarray, bucket_count: int):
    counts, _, tick_labels, bar_colors = compute_hue_statistics(rgb_image, bucket_count)

    fig_width = max(8.0, bucket_count * 0.45)
    fig, ax = plt.subplots(figsize=(fig_width, 4.6), dpi=120)
    fig.patch.set_facecolor("#fffdf7")
    ax.set_facecolor("#fffdf7")

    bars = ax.bar(
        np.arange(bucket_count),
        counts,
        width=0.86,
        color=bar_colors,
        edgecolor=bar_colors,
        linewidth=1.8,
    )

    for bar, color in zip(bars, bar_colors):
        bar.set_facecolor((*color, 0.22))
        bar.set_edgecolor(color)
        bar.set_hatch("////")
        bar.set_linewidth(1.8)

    ax.set_title(
        f"Pixel Counts Across {bucket_count} Hue Classes",
        fontsize=14,
        fontweight="bold",
        color="#1f2a33",
        pad=14,
    )
    ax.set_xlabel("Hue Class", fontsize=11, color="#31404d")
    ax.set_ylabel("Pixel Count", fontsize=11, color="#31404d")
    ax.set_xticks(np.arange(bucket_count))
    ax.set_xticklabels(tick_labels, rotation=45 if bucket_count > 10 else 0, ha="right")
    ax.grid(axis="y", linestyle=":", linewidth=0.9, alpha=0.35)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#9e9788")
    ax.spines["bottom"].set_color("#9e9788")
    ax.tick_params(colors="#44515c")
    ax.margins(x=0.01)
    plt.tight_layout()
    return fig


def load_image(file_path: str | None, bucket_count: int):
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


def refresh_histogram(bucket_count: int, rgb_image: np.ndarray | None):
    if rgb_image is None:
        return None
    return build_histogram(np.array(rgb_image), int(bucket_count))


def reset_app():
    return (
        None,
        None,
        None,
        None,
        DEFAULT_BUCKETS,
        gr.update(visible=True),
        gr.update(visible=False),
    )


def create_demo() -> gr.Blocks:
    with gr.Blocks(title="Hue Bucket Histogram") as demo:
        image_state = gr.State(None)

        with gr.Column(elem_classes=["hero-card"]):
            gr.Markdown(
                """
                # JPG Color Bucket Explorer
                Upload a `.jpg` image, choose a value `X` from **3 to 30**, and see how many pixels land in each hue class.

                With `X = 3`, the buckets are centered on **red**, **green**, and **blue**. Larger `X` values split the hue wheel into finer color families.
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

        upload_input.change(
            fn=load_image,
            inputs=[upload_input, bucket_slider],
            outputs=[
                image_state,
                image_preview,
                histogram_plot,
                upload_panel,
                result_sections,
            ],
        )

        bucket_slider.change(
            fn=refresh_histogram,
            inputs=[bucket_slider, image_state],
            outputs=histogram_plot,
        )

        redo_button.click(
            fn=reset_app,
            inputs=[],
            outputs=[
                upload_input,
                image_state,
                image_preview,
                histogram_plot,
                bucket_slider,
                upload_panel,
                result_sections,
            ],
        )

    return demo


