"""Calibration sanity checks: reprojection error."""

from __future__ import annotations

import numpy as np

from smartpi.vision.calibrate import apply_homography, load_calibration


def reprojection_error(
    calibration_path: str,
    src_pts: list[tuple[float, float]],
    dst_pts: list[tuple[float, float]],
) -> float | None:
    """Compute median reprojection error (pixels) for calibration validation.

    Args:
        calibration_path: Path to calibration.yaml.
        src_pts: Camera-space points.
        dst_pts: Expected projector-space points (same order).

    Returns:
        Median error in pixels, or None if calibration missing / invalid.
    """
    cal = load_calibration(calibration_path)
    if not cal or len(src_pts) != len(dst_pts):
        return None
    H = cal["homography"]
    errors = []
    for (sx, sy), (dx, dy) in zip(src_pts, dst_pts):
        px, py = apply_homography(H, sx, sy)
        err = np.hypot(px - dx, py - dy)
        errors.append(err)
    return float(np.median(errors)) if errors else None
