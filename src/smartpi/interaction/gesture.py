"""Tap, drag, long-press from pointer state stream."""

from __future__ import annotations

import time
from typing import Iterator

from smartpi.interaction.events import PointerEvent, PointerState

TAP_TIME_THRESHOLD = 0.3  # seconds
TAP_DISTANCE_THRESHOLD = 20.0  # pixels
LONG_PRESS_TIME = 0.5  # seconds


def classify_gesture(events: list[PointerEvent]) -> str:
    """Classify a short sequence of events as 'tap', 'drag', or 'long_press'.

    Simplification: expects events in order (down, optional move, up).
    """
    if not events:
        return "none"
    states = [e.state for e in events]
    if PointerState.DOWN not in states or PointerState.UP not in states:
        return "none"
    down_ev = next(e for e in events if e.state == PointerState.DOWN)
    up_ev = next(e for e in reversed(events) if e.state == PointerState.UP)
    dt = up_ev.timestamp - down_ev.timestamp
    dx = up_ev.x - down_ev.x
    dy = up_ev.y - down_ev.y
    dist = (dx * dx + dy * dy) ** 0.5
    move_events = [e for e in events if e.state == PointerState.MOVE]
    if dt >= LONG_PRESS_TIME:
        return "long_press"
    if dist > TAP_DISTANCE_THRESHOLD or len(move_events) > 2:
        return "drag"
    return "tap"


def emit_events_from_track(
    xy: tuple[float, float] | None,
    prev_xy: tuple[float, float] | None,
    prev_down: bool,
) -> Iterator[PointerEvent]:
    """Yield PointerEvents from current tracked position. Caller tracks prev_xy and prev_down."""
    t = time.perf_counter()
    if xy is None:
        if prev_down:
            yield PointerEvent(prev_xy[0], prev_xy[1], PointerState.UP, t)
        return
    if prev_xy is None and not prev_down:
        yield PointerEvent(xy[0], xy[1], PointerState.DOWN, t)
    elif prev_xy is not None and (xy[0] != prev_xy[0] or xy[1] != prev_xy[1]):
        yield PointerEvent(xy[0], xy[1], PointerState.MOVE, t)
    # UP is emitted when xy becomes None (pointer lost)
