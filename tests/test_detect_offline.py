"""Offline detection tests: synthetic frame or data/samples/frames/ if present."""

import pytest
from pathlib import Path

import numpy as np


def test_detect_bright_point_on_synthetic_frame():
    """Detector returns bright point on synthetic frame (no camera)."""
    from smartpi.vision.detect_bright import detect_bright_point

    # 100x100 frame with single bright pixel at (50, 50)
    frame = np.zeros((100, 100, 3), dtype=np.uint8)
    frame[50, 50] = [255, 255, 255]
    pt = detect_bright_point(frame, threshold=200)
    assert pt is not None
    assert abs(pt[0] - 50) <= 1 and abs(pt[1] - 50) <= 1


def test_detect_bright_point_below_threshold_returns_none():
    """Detector returns None when no pixel exceeds threshold."""
    from smartpi.vision.detect_bright import detect_bright_point

    frame = np.zeros((100, 100, 3), dtype=np.uint8)
    frame[50, 50] = [50, 50, 50]
    pt = detect_bright_point(frame, threshold=200)
    assert pt is None


@pytest.mark.skipif(
    not list((Path(__file__).parent.parent / "data" / "samples" / "frames").glob("*.png")),
    reason="No sample frame in data/samples/frames/",
)
def test_detect_on_sample_frame():
    """Run detector on first sample frame in data/samples/frames/ (regression)."""
    import cv2
    from smartpi.vision.detect_bright import detect_bright_point

    frames_dir = Path(__file__).parent.parent / "data" / "samples" / "frames"
    sample = next(frames_dir.glob("*.png"), None)
    if sample is None:
        pytest.skip("No PNG in data/samples/frames/")
    frame = cv2.imread(str(sample))
    assert frame is not None
    pt = detect_bright_point(frame, threshold=100)
    # Just ensure it doesn't crash; pt may be None if image has no bright spot
    assert pt is None or (isinstance(pt[0], (int, float)) and isinstance(pt[1], (int, float)))
