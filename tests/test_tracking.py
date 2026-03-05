"""Tests for smoothing tracker."""

import pytest

from smartpi.vision.track import SmoothingTracker


def test_tracker_first_update_returns_point():
    """First update sets internal state and returns the point."""
    t = SmoothingTracker(alpha=0.3)
    x, y = t.update(100.0, 200.0)
    assert (x, y) == (100.0, 200.0)


def test_tracker_smoothing():
    """Repeated updates smooth toward new position."""
    t = SmoothingTracker(alpha=0.5)
    t.update(0.0, 0.0)
    x, y = t.update(100.0, 0.0)
    assert 0 < x < 100
    assert y == 0.0


def test_tracker_reset():
    """Reset clears state; next update is treated as first."""
    t = SmoothingTracker(alpha=0.3)
    t.update(10.0, 20.0)
    t.reset()
    x, y = t.update(50.0, 60.0)
    assert (x, y) == (50.0, 60.0)
