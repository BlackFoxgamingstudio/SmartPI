"""Normalized pointer events."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class PointerState(str, Enum):
    """Pointer state: down, move, up."""

    DOWN = "down"
    MOVE = "move"
    UP = "up"


@dataclass
class PointerEvent:
    """Single pointer event in projector space."""

    x: float
    y: float
    state: PointerState
    timestamp: float
    confidence: float = 1.0
