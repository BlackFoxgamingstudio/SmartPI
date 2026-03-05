"""Particle Field: pointer pushes particles."""

from __future__ import annotations

import math
import random

import pygame


class Particle:
    """Simple particle with position and velocity."""

    __slots__ = ("x", "y", "vx", "vy", "radius")

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0
        self.radius = 4

    def push(self, px: float, py: float, strength: float = 80.0) -> None:
        dx = self.x - px
        dy = self.y - py
        d = math.hypot(dx, dy)
        if d < 1:
            d = 1
        f = strength / (d * d)
        self.vx += (dx / d) * f
        self.vy += (dy / d) * f

    def update(self, width: int, height: int, damping: float = 0.98) -> None:
        self.x += self.vx
        self.y += self.vy
        self.vx *= damping
        self.vy *= damping
        if self.x < 0 or self.x > width:
            self.vx *= -0.5
            self.x = max(0, min(width, self.x))
        if self.y < 0 or self.y > height:
            self.vy *= -0.5
            self.y = max(0, min(height, self.y))


class ParticleFieldScene:
    """Particles that are pushed by the pointer."""

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.particles: list[Particle] = []
        n = 80
        for _ in range(n):
            self.particles.append(
                Particle(
                    random.randint(0, width),
                    random.randint(0, height),
                )
            )
        self.pointer_xy: tuple[float, float] | None = None

    def on_pointer(self, ev: dict) -> None:
        state = ev.get("state", "")
        self.pointer_xy = (ev["x"], ev["y"])
        if state in ("down", "move"):
            for p in self.particles:
                p.push(ev["x"], ev["y"])
        if state == "up":
            self.pointer_xy = None

    def update(self) -> None:
        for p in self.particles:
            p.update(self.width, self.height)

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill((15, 15, 25))
        for p in self.particles:
            pygame.draw.circle(surface, (100, 150, 255), (int(p.x), int(p.y)), p.radius)
        if self.pointer_xy:
            pygame.draw.circle(surface, (255, 255, 0), (int(self.pointer_xy[0]), int(self.pointer_xy[1])), 12, 2)
