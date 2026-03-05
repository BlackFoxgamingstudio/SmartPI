"""4-point auto-calibration: homography solve and persistence for camera -> projector mapping.

Maps the camera's field of view to the projector display area via four point
correspondences (e.g. four corners). Used in the motion-to-input pipeline
(Capture -> Process -> Interact / Kiosk web UI).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import cv2
import numpy as np
import yaml


def solve_homography(
    src_pts: list[tuple[float, float]],
    dst_pts: list[tuple[float, float]],
) -> np.ndarray | None:
    """Compute 3x3 homography from 4+ point correspondences.

    Args:
        src_pts: Camera-space points (e.g. [(x1,y1), ...]).
        dst_pts: Projector-space points (same order).

    Returns:
        3x3 homography matrix or None if insufficient points or singular.
    """
    if len(src_pts) < 4 or len(dst_pts) < 4:
        return None
    src = np.array(src_pts, dtype=np.float32)
    dst = np.array(dst_pts, dtype=np.float32)
    H, status = cv2.findHomography(src, dst, cv2.RANSAC, 5.0)
    return H


def save_calibration(
    path: str | Path,
    homography: np.ndarray,
    bounds: tuple[int, int, int, int],
    resolution: tuple[int, int],
) -> None:
    """Save calibration to YAML. Do not commit this file.

    Args:
        path: Output file path.
        homography: 3x3 matrix.
        bounds: (x0, y0, x1, y1) projector pixel bounds.
        resolution: (width, height) of projector at calibration.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    data: dict[str, Any] = {
        "homography": homography.tolist(),
        "bounds": list(bounds),
        "resolution": list(resolution),
    }
    with open(path, "w") as f:
        yaml.safe_dump(data, f, default_flow_style=False)


def load_calibration(path: str | Path) -> dict[str, Any] | None:
    """Load calibration YAML. Returns dict with homography, bounds, resolution or None."""
    path = Path(path)
    if not path.exists():
        return None
    with open(path) as f:
        data = yaml.safe_load(f)
    if not data or "homography" not in data:
        return None
    data["homography"] = np.array(data["homography"], dtype=np.float64)
    return data


def apply_homography(H: np.ndarray, x: float, y: float) -> tuple[float, float]:
    """Map camera (x,y) to projector coordinates using homography H."""
    pt = np.array([[x, y]], dtype=np.float32)
    out = cv2.perspectiveTransform(pt.reshape(1, 1, 2), H)
    return (float(out[0, 0, 0]), float(out[0, 0, 1]))
