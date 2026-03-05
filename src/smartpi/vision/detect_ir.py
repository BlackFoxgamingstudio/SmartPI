"""IR blob detector: threshold + morphology -> single brightest blob."""

from __future__ import annotations

import cv2
import numpy as np

from smartpi.vision.preprocess import preprocess_grayscale, threshold_mask


def detect_ir_blob(
    frame: np.ndarray,
    threshold: int = 200,
    blur_ksize: int = 3,
    morph_ksize: int = 5,
) -> tuple[float, float] | None:
    """Detect the brightest IR blob (e.g. IR pen tip). Returns (x, y) or None.

    Args:
        frame: BGR or grayscale frame (IR-sensitive camera).
        threshold: Pixels above this become candidates.
        blur_ksize: Pre-blur kernel size (odd).
        morph_ksize: Morphology kernel size for cleaning (odd).

    Returns:
        Center (x, y) of largest blob in image coordinates, or None.
    """
    gray = preprocess_grayscale(frame, blur_ksize)
    mask = threshold_mask(gray, threshold)
    if morph_ksize > 0 and morph_ksize % 2 == 1:
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (morph_ksize, morph_ksize))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    contours, _ = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    if not contours:
        return None
    largest = max(contours, key=cv2.contourArea)
    if cv2.contourArea(largest) < 10:
        return None
    M = cv2.moments(largest)
    if M["m00"] == 0:
        return None
    cx = M["m10"] / M["m00"]
    cy = M["m01"] / M["m00"]
    return (float(cx), float(cy))
