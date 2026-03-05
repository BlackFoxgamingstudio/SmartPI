"""FPS and frame timing utilities."""

import time
from collections import deque


class FPSCounter:
    """Simple FPS counter using a sliding window of frame timestamps."""

    def __init__(self, window_size: int = 30) -> None:
        """Initialize with a window of recent frame times.

        Args:
            window_size: Number of frames to average over for FPS.
        """
        self._times: deque[float] = deque(maxlen=window_size)

    def tick(self) -> None:
        """Record a frame (call once per frame)."""
        self._times.append(time.perf_counter())

    def fps(self) -> float:
        """Return current FPS (0 if fewer than 2 samples)."""
        if len(self._times) < 2:
            return 0.0
        elapsed = self._times[-1] - self._times[0]
        if elapsed <= 0:
            return 0.0
        return (len(self._times) - 1) / elapsed
