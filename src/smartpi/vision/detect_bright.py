"""Visible bright spot detector (HSV/brightness threshold)."""

from __future__ import annotations

import cv2
import numpy as np

from smartpi.vision.preprocess import preprocess_grayscale


def detect_bright_point(
    frame: np.ndarray,
    threshold: int = 200,
    blur_ksize: int = 3,
) -> tuple[float, float] | None:
    """Detect the brightest point (e.g. laser or LED). Returns (x, y) or None.

    Uses grayscale max; for colored spots consider HSV. Single global max for speed.

    Args:
        frame: BGR frame.
        threshold: Minimum brightness to consider.
        blur_ksize: Pre-blur (odd); 0 to skip.

    Returns:
        Center (x, y) of bright spot, or None.
    """
    gray = preprocess_grayscale(frame, blur_ksize)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(gray)
    if max_val < threshold:
        return None
    return (float(max_loc[0]), float(max_loc[1]))
