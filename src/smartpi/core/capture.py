"""Camera capture abstraction (OpenCV or optional libcamera via Picamera2). Config-driven."""

from __future__ import annotations

from typing import Any

import cv2
import numpy as np


def create_capture(
    camera_index: int = 0,
    width: int = 640,
    height: int = 480,
    fps: float = 30.0,
    use_libcamera: bool = False,
) -> "CameraCapture | LibcameraCapture":
    """Create a capture instance. If use_libcamera is True and Picamera2 is available, returns LibcameraCapture; else CameraCapture."""
    if use_libcamera:
        try:
            return LibcameraCapture(width=width, height=height, fps=fps)
        except ImportError:
            pass
    return CameraCapture(camera_index=camera_index, width=width, height=height, fps=fps)


class LibcameraCapture:
    """Capture frames via libcamera (Picamera2). Use when use_libcamera is True and picamera2 is installed (e.g. on Raspberry Pi)."""

    def __init__(self, width: int = 640, height: int = 480, fps: float = 30.0) -> None:
        self.width = width
        self.height = height
        self.fps = fps
        self._picam2: Any = None

    def open(self) -> bool:
        try:
            from picamera2 import Picamera2
            self._picam2 = Picamera2()
            config = self._picam2.create_video_configuration(
                main={"size": (self.width, self.height), "format": "BGR888"}
            )
            self._picam2.configure(config)
            self._picam2.start()
            return True
        except (ImportError, Exception):
            return False

    def read(self) -> tuple[bool, np.ndarray | None]:
        if self._picam2 is None:
            return False, None
        try:
            frame = self._picam2.capture_array()
            if frame is None:
                return False, None
            return True, frame
        except Exception:
            return False, None

    def release(self) -> None:
        if self._picam2 is not None:
            try:
                self._picam2.stop()
            except Exception:
                pass
            self._picam2 = None

    def __enter__(self) -> "LibcameraCapture":
        self.open()
        return self

    def __exit__(self, *args: Any) -> None:
        self.release()


class CameraCapture:
    """Capture frames from a camera device. Uses OpenCV VideoCapture."""

    def __init__(
        self,
        camera_index: int = 0,
        width: int = 640,
        height: int = 480,
        fps: float = 30.0,
    ) -> None:
        """Initialize capture with device index and resolution.

        Args:
            camera_index: OpenCV camera device index (0, 1, ...).
            width: Frame width in pixels.
            height: Frame height in pixels.
            fps: Target FPS (may not be achieved depending on driver).
        """
        self.camera_index = camera_index
        self.width = width
        self.height = height
        self.fps = fps
        self._cap: cv2.VideoCapture | None = None

    def open(self) -> bool:
        """Open the camera. Returns True if successful."""
        self._cap = cv2.VideoCapture(self.camera_index)
        if not self._cap.isOpened():
            return False
        self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self._cap.set(cv2.CAP_PROP_FPS, self.fps)
        return True

    def read(self) -> tuple[bool, np.ndarray | None]:
        """Read one frame. Returns (success, frame). Frame is BGR or None on failure."""
        if self._cap is None or not self._cap.isOpened():
            return False, None
        ret, frame = self._cap.read()
        if not ret or frame is None:
            return False, None
        return True, frame

    def release(self) -> None:
        """Release the camera."""
        if self._cap is not None:
            self._cap.release()
            self._cap = None

    def __enter__(self) -> CameraCapture:
        self.open()
        return self

    def __exit__(self, *args: Any) -> None:
        self.release()
