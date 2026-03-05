"""Feed PointerEvents into Pygame (e.g. for scene logic)."""

from __future__ import annotations

from typing import Callable

from smartpi.interaction.events import PointerEvent


def pygame_event_from_pointer(ev: PointerEvent) -> dict:
    """Convert PointerEvent to a dict that scene code can use like a Pygame event."""
    return {
        "type": "pointer",
        "x": ev.x,
        "y": ev.y,
        "state": ev.state.value,
        "timestamp": ev.timestamp,
    }


def push_to_pygame(ev: PointerEvent, callback: Callable[[dict], None]) -> None:
    """Push a PointerEvent to a callback (e.g. scene.on_pointer)."""
    callback(pygame_event_from_pointer(ev))
