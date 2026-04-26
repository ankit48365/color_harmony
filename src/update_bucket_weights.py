"""Editable table callback helpers for weighted bucket saturation changes."""

from __future__ import annotations

import numpy as np

from bucket_details import BucketDetailsTable, BucketOutputs, build_bucket_outputs


def update_bucket_weights(
    bucket_details: BucketDetailsTable | None,
    bucket_count: int,
    rgb_image: np.ndarray | None,
) -> BucketOutputs:
    """Apply the edited weight column and return the synchronized histogram/table."""

    if rgb_image is None:
        return None, None, []

    return build_bucket_outputs(int(bucket_count), np.array(rgb_image), bucket_details)
