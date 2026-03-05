"""Sandbox Draw: IR pen draws ink; corner hotzones for color."""

from __future__ import annotations

import pygame


class SandboxDrawScene:
    """Drawing scene: pointer draws lines; corners switch color."""

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.lines: list[list[tuple[int, int]]] = []
        self.current_stroke: list[tuple[int, int]] = []
        self.color = (255, 255, 255)
        self.colors = [(255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
        self.color_index = 0

    def on_pointer(self, ev: dict) -> None:
        """Handle pointer event: down starts stroke, move adds point, up ends stroke."""
        x, y = int(ev["x"]), int(ev["y"])
        state = ev.get("state", "")
        # Corner hotzones: switch color
        margin = min(self.width, self.height) // 8
        if x < margin and y < margin:
            self.color_index = (self.color_index + 1) % len(self.colors)
            self.color = self.colors[self.color_index]
            return
        if state == "down":
            self.current_stroke = [(x, y)]
        elif state == "move" and self.current_stroke:
            self.current_stroke.append((x, y))
        elif state == "up" and self.current_stroke:
            self.current_stroke.append((x, y))
            self.lines.append(self.current_stroke)
            self.current_stroke = []

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill((20, 20, 30))
        for stroke in self.lines:
            if len(stroke) < 2:
                continue
            pygame.draw.lines(surface, self.color, False, stroke, 4)
        if len(self.current_stroke) >= 2:
            pygame.draw.lines(surface, self.color, False, self.current_stroke, 4)
        # Corner hint
        font = pygame.font.Font(None, 24)
        text = font.render("Top-left: change color", True, (180, 180, 180))
        surface.blit(text, (10, self.height - 30))
