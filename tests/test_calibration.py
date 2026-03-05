"""Tests for homography solve and calibration load/save."""

import numpy as np
import pytest
from pathlib import Path

from smartpi.vision.calibrate import (
    solve_homography,
    save_calibration,
    load_calibration,
    apply_homography,
)


def test_solve_homography_identity():
    """Identity-like correspondences yield near-identity homography."""
    src = [(0, 0), (100, 0), (100, 100), (0, 100)]
    dst = [(0, 0), (100, 0), (100, 100), (0, 100)]
    H = solve_homography(src, dst)
    assert H is not None
    np.testing.assert_allclose(H, np.eye(3), atol=1e-2)


def test_solve_homography_insufficient_points():
    """Fewer than 4 points returns None."""
    src = [(0, 0), (1, 0), (1, 1)]
    dst = [(0, 0), (1, 0), (1, 1)]
    assert solve_homography(src, dst) is None


def test_apply_homography_identity():
    """With identity H, point is unchanged."""
    H = np.eye(3)
    x, y = apply_homography(H, 50.0, 50.0)
    assert abs(x - 50.0) < 1e-5 and abs(y - 50.0) < 1e-5


def test_save_and_load_calibration(tmp_path):
    """Save calibration then load returns same homography and bounds."""
    H = np.eye(3)
    H[0, 2] = 10
    bounds = (0, 0, 1920, 1080)
    res = (1920, 1080)
    out = tmp_path / "cal.yaml"
    save_calibration(out, H, bounds, res)
    assert out.exists()
    loaded = load_calibration(out)
    assert loaded is not None
    np.testing.assert_allclose(loaded["homography"], H)
    assert loaded["bounds"] == list(bounds)
    assert loaded["resolution"] == list(res)


def test_load_calibration_missing_returns_none(tmp_path):
    """Loading non-existent file returns None."""
    assert load_calibration(tmp_path / "nonexistent.yaml") is None
