"""Helpers that synchronize the histogram and editable bucket detail table."""

from __future__ import annotations

from typing import Any

import numpy as np
from matplotlib.figure import Figure

from build_histogram import build_histogram_from_statistics
from compute_hue_statistics import (
    DEFAULT_SATURATION_WEIGHT,
    analyze_hue_buckets,
    build_adjusted_preview_image,
    compute_bucket_table_rows_from_statistics,
    normalize_saturation_weights,
)

BucketDetailCell = str | int | float | None
BucketDetailsTable = list[list[BucketDetailCell]]
BucketOutputs = tuple[np.ndarray | None, Figure | None, BucketDetailsTable]


def extract_saturation_weights(
    bucket_details: BucketDetailsTable | None,
    bucket_count: int,
) -> list[int]:
    """Read the editable weight column from the table and sanitize it."""

    if not bucket_details:
        return normalize_saturation_weights(bucket_count)

    raw_weights: list[Any] = []
    for row in bucket_details[:bucket_count]:
        if isinstance(row, (list, tuple)) and len(row) >= 3:
            raw_weights.append(row[2])
        else:
            raw_weights.append(DEFAULT_SATURATION_WEIGHT)

    return normalize_saturation_weights(bucket_count, raw_weights)


def build_bucket_outputs(
    bucket_count: int,
    rgb_image: np.ndarray | None,
    bucket_details: BucketDetailsTable | None = None,
) -> BucketOutputs:
    """Build the histogram and editable bucket table from a shared analysis pass."""

    if rgb_image is None:
        return None, None, []

    rgb_array = np.array(rgb_image)
    weights = extract_saturation_weights(bucket_details, int(bucket_count))
    statistics = analyze_hue_buckets(rgb_array, int(bucket_count), weights)
    return (
        build_adjusted_preview_image(statistics, rgb_array.shape),
        build_histogram_from_statistics(statistics),
        compute_bucket_table_rows_from_statistics(statistics),
    )
