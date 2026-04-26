from __future__ import annotations

import app
import gradio_app
import numpy as np

from bucket_details import build_bucket_outputs
from compute_hue_statistics import compute_hue_statistics


def test_entrypoint_modules_import_cleanly() -> None:
    assert callable(app.main)
    assert callable(gradio_app.create_demo)


def test_three_bucket_classification_matches_rgb_primaries() -> None:
    rgb_image = np.array([[[255, 0, 0], [0, 255, 0], [0, 0, 255]]], dtype=np.uint8)

    counts, centers, tick_labels, bar_colors = compute_hue_statistics(rgb_image, 3)

    assert counts.tolist() == [1, 1, 1]
    assert [int(round(center)) for center in centers.tolist()] == [0, 120, 240]
    assert tick_labels == ["Red", "Green", "Blue"]
    assert bar_colors.shape == (3, 3)


def test_bucket_counts_cover_every_pixel_for_finer_splits() -> None:
    rgb_image = np.array(
        [
            [[255, 0, 0], [255, 255, 0]],
            [[0, 255, 255], [255, 0, 255]],
        ],
        dtype=np.uint8,
    )

    counts, centers, tick_labels, bar_colors = compute_hue_statistics(rgb_image, 20)

    assert counts.sum() == 4
    assert len(counts) == 20
    assert len(centers) == 20
    assert len(tick_labels) == 20
    assert bar_colors.shape == (20, 3)


def test_saturation_weights_change_bucket_colors() -> None:
    rgb_image = np.array([[[255, 0, 0], [0, 255, 0], [0, 0, 255]]], dtype=np.uint8)

    baseline_counts, _, _, baseline_colors = compute_hue_statistics(
        rgb_image,
        3,
        saturation_weights=[50, 50, 50],
    )
    desaturated_counts, _, _, desaturated_colors = compute_hue_statistics(
        rgb_image,
        3,
        saturation_weights=[0, 50, 50],
    )
    saturated_counts, _, _, saturated_colors = compute_hue_statistics(
        rgb_image,
        3,
        saturation_weights=[100, 50, 50],
    )

    assert baseline_counts.tolist() == desaturated_counts.tolist() == saturated_counts.tolist()
    assert baseline_counts.tolist() == [1, 1, 1]
    assert np.allclose(desaturated_colors[0][0], desaturated_colors[0][1])
    assert baseline_colors[0][0] > baseline_colors[0][1]
    assert saturated_colors[0][1] < baseline_colors[0][1]
    assert saturated_colors[0][0] > saturated_colors[0][1]
    assert saturated_colors[0][1] == saturated_colors[0][2]


def test_bucket_outputs_update_preview_image_hex_codes_and_sanitized_weights() -> None:
    rgb_image = np.array(
        [[[200, 100, 100], [100, 200, 100], [100, 100, 200]]],
        dtype=np.uint8,
    )

    preview_image, figure, bucket_rows = build_bucket_outputs(
        3,
        rgb_image,
        bucket_details=[
            ["ignored", "ignored", 120],
            ["ignored", "ignored", -10],
            ["ignored", "ignored", "abc"],
        ],
    )

    assert preview_image is not None
    assert figure is not None
    assert preview_image.tolist() == [[[200, 0, 0], [200, 200, 200], [100, 100, 200]]]
    assert bucket_rows == [
        ["Red (#F20000)", "33.33%", 100],
        ["Green (#F2F2F2)", "33.33%", 0],
        ["Blue (#3D3DF2)", "33.33%", 50],
    ]
