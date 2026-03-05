"""Debug overlay: FPS, thresholds, pointer position."""

from __future__ import annotations

import pygame


def draw_overlay(
    surface: pygame.Surface,
    fps: float,
    pointer_xy: tuple[float, float] | None,
    threshold: int = 0,
) -> None:
    """Draw overlay text (FPS, pointer, threshold) on the given surface.

    Args:
        surface: Pygame surface (e.g. screen).
        fps: Current FPS value.
        pointer_xy: (x, y) in display coordinates or None.
        threshold: Current detection threshold (0 to hide).
    """
    font = pygame.font.Font(None, 36)
    lines = [f"FPS: {fps:.1f}"]
    if threshold > 0:
        lines.append(f"Thr: {threshold}")
    if pointer_xy is not None:
        lines.append(f"Ptr: {pointer_xy[0]:.0f}, {pointer_xy[1]:.0f}")
    y = 10
    for line in lines:
        text = font.render(line, True, (255, 255, 0))
        surface.blit(text, (10, y))
        y += 28
    if pointer_xy is not None:
        px, py = int(pointer_xy[0]), int(pointer_xy[1])
        pygame.draw.circle(surface, (0, 255, 0), (px, py), 8, 2)
