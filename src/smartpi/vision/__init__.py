"""Vision pipeline: preprocess, detect (IR/bright), track, calibrate, validate."""

from smartpi.vision.preprocess import preprocess_grayscale, threshold_mask
from smartpi.vision.detect_bright import detect_bright_point
from smartpi.vision.detect_ir import detect_ir_blob
from smartpi.vision.track import SmoothingTracker
from smartpi.vision.calibrate import solve_homography, load_calibration, save_calibration
from smartpi.vision.validate import reprojection_error

__all__ = [
    "preprocess_grayscale",
    "threshold_mask",
    "detect_bright_point",
    "detect_ir_blob",
    "SmoothingTracker",
    "solve_homography",
    "load_calibration",
    "save_calibration",
    "reprojection_error",
]
