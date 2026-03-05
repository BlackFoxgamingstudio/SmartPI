"""Temporal smoothing (EMA), optional Kalman, and velocity clamp for single-point tracking."""

from __future__ import annotations

import math


class SmoothingTracker:
    """EMA smoothing for a single 2D point. Optional Kalman filter or velocity clamp to reduce jitter."""

    def __init__(
        self,
        alpha: float = 0.3,
        max_velocity: float = 500.0,
        use_kalman: bool = False,
        process_noise: float = 1e-2,
        measurement_noise: float = 10.0,
    ) -> None:
        """Initialize tracker.

        Args:
            alpha: EMA factor (0--1). Used only when use_kalman is False. Smaller = smoother, more lag.
            max_velocity: Cap per-frame pixel movement (px/frame). Used only for EMA path.
            use_kalman: If True, use a 2D constant-velocity Kalman filter instead of EMA.
            process_noise: Kalman process noise (state uncertainty per step).
            measurement_noise: Kalman measurement noise (observation variance).
        """
        self.alpha = alpha
        self.max_velocity = max_velocity
        self.use_kalman = use_kalman
        self._process_noise = process_noise
        self._measurement_noise = measurement_noise
        self._x: float | None = None
        self._y: float | None = None
        # Kalman state: [x, y, vx, vy], P is 4x4 covariance
        self._kalman_state: list[float] | None = None
        self._kalman_P: list[list[float]] | None = None

    def update(self, x: float, y: float) -> tuple[float, float]:
        """Update with new detection. Returns smoothed (x, y)."""
        if self.use_kalman:
            return self._update_kalman(x, y)
        return self._update_ema(x, y)

    def _update_ema(self, x: float, y: float) -> tuple[float, float]:
        if self._x is None or self._y is None:
            self._x, self._y = x, y
            return (x, y)
        dx = x - self._x
        dy = y - self._y
        if self.max_velocity > 0:
            dist = math.hypot(dx, dy)
            if dist > self.max_velocity:
                scale = self.max_velocity / dist
                dx *= scale
                dy *= scale
        self._x += self.alpha * (x - self._x)
        self._y += self.alpha * (y - self._y)
        return (self._x, self._y)

    def _update_kalman(self, z_x: float, z_y: float) -> tuple[float, float]:
        import numpy as np
        # 2D constant-velocity: state = [x, y, vx, vy], measurement = [x, y]
        # F = [[1,0,1,0], [0,1,0,1], [0,0,1,0], [0,0,0,1]], H = [[1,0,0,0], [0,1,0,0]]
        if self._kalman_state is None or self._kalman_P is None:
            self._kalman_state = np.array([z_x, z_y, 0.0, 0.0], dtype=float)
            self._kalman_P = np.diag([self._measurement_noise, self._measurement_noise, 100.0, 100.0])
            self._x, self._y = z_x, z_y
            return (z_x, z_y)
        q, r = self._process_noise, self._measurement_noise
        F = np.array([[1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]], dtype=float)
        H = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], dtype=float)
        Q = np.eye(4) * q
        R = np.eye(2) * r
        state = np.asarray(self._kalman_state).reshape(4, 1)
        P = np.asarray(self._kalman_P)
        # Predict
        state = F @ state
        P = F @ P @ F.T + Q
        # Update
        z = np.array([[z_x], [z_y]])
        y = z - H @ state
        S = H @ P @ H.T + R
        K = P @ H.T @ np.linalg.inv(S)
        state = state + K @ y
        P = (np.eye(4) - K @ H) @ P
        self._kalman_state = state.ravel().tolist()
        self._kalman_P = P.tolist()
        self._x, self._y = float(state[0, 0]), float(state[1, 0])
        return (self._x, self._y)

    def reset(self) -> None:
        """Reset state (e.g. when pointer is lost)."""
        self._x = self._y = None
        self._kalman_state = None
        self._kalman_P = None
