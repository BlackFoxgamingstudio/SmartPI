"""STEM Widgets: ruler, angles, graph paper. Tap to place points; corner hotzones for mode and clear."""

from __future__ import annotations

import math
from typing import Literal

import pygame


Mode = Literal["ruler", "angles", "graph"]
MODES: list[Mode] = ["ruler", "angles", "graph"]
GRID_CELL_PX = 50  # graph paper cell size in pixels


class StemWidgetsScene:
    """Ruler (length), angles (degrees), and graph paper (grid + snap)."""

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.mode: Mode = "ruler"
        self.points: list[tuple[int, int]] = []
        self.ruler_segments: list[tuple[tuple[int, int], tuple[int, int]]] = []
        self.angle_triples: list[tuple[tuple[int, int], tuple[int, int], tuple[int, int]]] = []
        self.graph_visible = True
        self._font: pygame.font.Font | None = None

    def _font_small(self) -> pygame.font.Font:
        if self._font is None:
            self._font = pygame.font.Font(None, 24)
        return self._font

    def _corner_margin(self) -> int:
        return min(self.width, self.height) // 8

    def _in_top_left(self, x: int, y: int) -> bool:
        m = self._corner_margin()
        return x < m and y < m

    def _in_top_right(self, x: int, y: int) -> bool:
        m = self._corner_margin()
        return x >= self.width - m and y < m

    def _snap_to_grid(self, x: int, y: int) -> tuple[int, int]:
        sx = (x // GRID_CELL_PX) * GRID_CELL_PX
        sy = (y // GRID_CELL_PX) * GRID_CELL_PX
        return (sx, sy)

    def on_pointer(self, ev: dict) -> None:
        x, y = int(ev["x"]), int(ev["y"])
        state = ev.get("state", "")

        if self._in_top_left(x, y):
            if state == "down":
                idx = MODES.index(self.mode)
                self.mode = MODES[(idx + 1) % len(MODES)]
                self.points = []
            return
        if self._in_top_right(x, y):
            if state == "down":
                self.points = []
                if self.mode == "ruler":
                    self.ruler_segments = []
                elif self.mode == "angles":
                    self.angle_triples = []
            return

        if state != "down":
            return

        if self.mode == "graph":
            x, y = self._snap_to_grid(x, y)

        if self.mode == "ruler":
            self.points.append((x, y))
            if len(self.points) >= 2:
                self.ruler_segments.append((self.points[-2], self.points[-1]))
                self.points = []
        elif self.mode == "angles":
            self.points.append((x, y))
            if len(self.points) >= 3:
                self.angle_triples.append(
                    (self.points[-3], self.points[-2], self.points[-1])
                )
                self.points = []
        elif self.mode == "graph":
            self.points.append((x, y))

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill((30, 35, 40))
        font = self._font_small()

        if self.mode == "graph" and self.graph_visible:
            for gx in range(0, self.width + 1, GRID_CELL_PX):
                pygame.draw.line(surface, (50, 55, 60), (gx, 0), (gx, self.height), 1)
            for gy in range(0, self.height + 1, GRID_CELL_PX):
                pygame.draw.line(surface, (50, 55, 60), (0, gy), (self.width, gy), 1)

        for (a, b) in self.ruler_segments:
            pygame.draw.line(surface, (200, 200, 255), a, b, 3)
            mid = ((a[0] + b[0]) // 2, (a[1] + b[1]) // 2)
            length_px = math.hypot(b[0] - a[0], b[1] - a[1])
            label = f"{length_px:.0f} px"
            text = font.render(label, True, (220, 220, 255))
            surface.blit(text, (mid[0] - text.get_width() // 2, mid[1] - 14))

        for (v, p1, p2) in self.angle_triples:
            pygame.draw.line(surface, (200, 255, 200), v, p1, 3)
            pygame.draw.line(surface, (200, 255, 200), v, p2, 3)
            u1 = (p1[0] - v[0], p1[1] - v[1])
            u2 = (p2[0] - v[0], p2[1] - v[1])
            d1 = math.hypot(u1[0], u1[1]) or 1
            d2 = math.hypot(u2[0], u2[1]) or 1
            cos_a = (u1[0] * u2[0] + u1[1] * u2[1]) / (d1 * d2)
            cos_a = max(-1, min(1, cos_a))
            deg = math.degrees(math.acos(cos_a))
            cx = (v[0] + p1[0] + p2[0]) // 3
            cy = (v[1] + p1[1] + p2[1]) // 3
            text = font.render(f"{deg:.1f}°", True, (200, 255, 200))
            surface.blit(text, (cx - text.get_width() // 2, cy - 12))

        for (x, y) in self.points:
            pygame.draw.circle(surface, (200, 200, 255), (x, y), 8)

        if self.mode == "ruler" and len(self.points) == 1:
            pygame.draw.circle(surface, (200, 200, 255), self.points[0], 8)
            tip = font.render("Tap again for end point", True, (180, 180, 200))
            surface.blit(tip, (self.points[0][0] + 12, self.points[0][1] - 10))
        if self.mode == "angles" and len(self.points) == 1:
            tip = font.render("Tap for first ray", True, (180, 220, 180))
            surface.blit(tip, (self.points[0][0] + 12, self.points[0][1] - 10))
        if self.mode == "angles" and len(self.points) == 2:
            tip = font.render("Tap for second ray", True, (180, 220, 180))
            surface.blit(tip, (self.points[1][0] + 12, self.points[1][1] - 10))

        m = self._corner_margin()
        mode_label = font.render(f"Mode: {self.mode}", True, (200, 200, 200))
        surface.blit(mode_label, (10, self.height - 50))
        surface.blit(font.render("Top-left: mode", True, (160, 160, 160)), (10, self.height - 28))
        surface.blit(font.render("Top-right: clear", True, (160, 160, 160)), (self.width - 120, 10))
