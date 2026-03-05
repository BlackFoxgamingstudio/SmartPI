"""Tests for pointer events and gesture classification."""

import pytest
import time

from smartpi.interaction.events import PointerEvent, PointerState
from smartpi.interaction.gesture import classify_gesture, emit_events_from_track


def test_pointer_event_creation():
    """PointerEvent has required fields."""
    ev = PointerEvent(10.0, 20.0, PointerState.DOWN, time.perf_counter())
    assert ev.x == 10.0 and ev.y == 20.0
    assert ev.state == PointerState.DOWN


def test_classify_gesture_tap():
    """Short down->up with little movement is tap."""
    t = time.perf_counter()
    events = [
        PointerEvent(0, 0, PointerState.DOWN, t),
        PointerEvent(5, 5, PointerState.UP, t + 0.1),
    ]
    assert classify_gesture(events) == "tap"


def test_classify_gesture_drag():
    """Down, move, up with significant movement is drag."""
    t = time.perf_counter()
    events = [
        PointerEvent(0, 0, PointerState.DOWN, t),
        PointerEvent(50, 0, PointerState.MOVE, t + 0.05),
        PointerEvent(100, 0, PointerState.UP, t + 0.1),
    ]
    assert classify_gesture(events) == "drag"


def test_emit_events_from_track_down_when_new_pointer():
    """When prev_xy is None and we get pointer, emit DOWN."""
    events = list(emit_events_from_track((10.0, 20.0), None, False))
    assert len(events) == 1
    assert events[0].state == PointerState.DOWN
    assert events[0].x == 10.0 and events[0].y == 20.0


def test_emit_events_from_track_up_when_pointer_lost():
    """When pointer is None and prev_down, emit UP."""
    events = list(emit_events_from_track(None, (10.0, 20.0), True))
    assert len(events) == 1
    assert events[0].state == PointerState.UP
