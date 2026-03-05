"""Preprocessing: grayscale, blur, threshold, masks."""

from __future__ import annotations

import cv2
import numpy as np


def preprocess_grayscale(frame: np.ndarray, blur_ksize: int = 3) -> np.ndarray:
    """Convert to grayscale and optionally blur.

    Args:
        frame: BGR or grayscale frame.
        blur_ksize: Kernel size for Gaussian blur (odd); 0 to skip.

    Returns:
        Grayscale uint8 image.
    """
    if len(frame.shape) == 3:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    else:
        gray = frame.copy()
    if blur_ksize > 0 and blur_ksize % 2 == 1:
        gray = cv2.GaussianBlur(gray, (blur_ksize, blur_ksize), 0)
    return gray


def threshold_mask(gray: np.ndarray, threshold: int) -> np.ndarray:
    """Binary mask where pixel >= threshold.

    Args:
        gray: Grayscale image.
        threshold: Value in 0--255.

    Returns:
        Binary uint8 mask (0 or 255).
    """
    _, mask = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    return mask
