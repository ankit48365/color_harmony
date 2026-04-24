from __future__ import annotations

import app
import gradio_app
import numpy as np

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
