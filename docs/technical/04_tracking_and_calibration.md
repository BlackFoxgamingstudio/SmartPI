# Tracking and Calibration: Logic and Data In/Out

This document describes the tracking layer (temporal smoothing of the 2D pointer position) and the full calibration subsystem (homography solve, save/load, apply, and validation). Every function’s inputs, outputs, and logic are specified.

## Role of tracking

Detection yields a raw (x, y) every frame, which can jitter. The tracker smooths this either with an exponential moving average (EMA) and optional velocity clamp, or with an optional 2D constant-velocity Kalman filter when `use_kalman` is True. In the main app, tracking is applied in **projector space** (after homography); in the calibration wizard, camera-space points are not smoothed by this tracker. The tracker is single-pointer: one (x, y) in, one (x, y) out per frame.

## Role of calibration

Calibration establishes the mapping from camera image coordinates to projector pixel coordinates. It is done once (or when the setup changes) via the calibration wizard: the user taps four corners in a known order, the wizard collects four camera-space points, and a 3×3 homography is solved from these to fixed projector corners. The result is saved to `configs/calibration.yaml`. At runtime, every detected camera-space point is transformed with this homography before being passed to the tracker and event layer. Validation (reprojection error) can be run after calibration to check quality.

---

## Tracking: `SmoothingTracker` class

**Module:** `smartpi.vision.track`  
**Class:** `SmoothingTracker`

### Constructor: `__init__(self, alpha=0.3, max_velocity=500.0, use_kalman=False, process_noise=1e-2, measurement_noise=10.0)`

**Inputs:**  
- `alpha` (float): EMA factor in (0, 1]. Used only when `use_kalman` is False. Smaller = smoother but more lag.  
- `max_velocity` (float): Maximum allowed movement per frame in pixels; 0 to disable clamping. Used only for EMA path.  
- `use_kalman` (bool): If True, use a 2D constant-velocity Kalman filter instead of EMA.  
- `process_noise` (float): Kalman process noise (state uncertainty per step).  
- `measurement_noise` (float): Kalman measurement noise (observation variance).

**Outputs:** None. Initializes internal state to None so the first `update` is treated as “first sample.”

**Logic:** Store parameters; set `self._x`, `self._y` to None (and Kalman state/P to None when use_kalman).

### Method: `update(self, x, y) -> tuple[float, float]`

**Inputs:** `x`, `y` (float): current position (projector space in main app).

**Outputs:** Smoothed (x, y) as a tuple of two floats.

**Logic:** If `use_kalman` is True, the implementation calls `_update_kalman(x, y)` (see “Optional Kalman filter” below). Otherwise it uses the EMA path:  
1. If `self._x is None` or `self._y is None`: set `self._x, self._y = x, y` and return `(x, y)` (no smoothing on first sample).  
2. Compute displacement: `dx = x - self._x`, `dy = y - self._y`.  
3. If `max_velocity > 0`: compute `dist = hypot(dx, dy)`; if `dist > max_velocity`, scale: `scale = max_velocity / dist`, `dx *= scale`, `dy *= scale`. So the *incoming* (x, y) is effectively clamped toward the previous position before applying EMA.  
4. EMA update: `self._x += self.alpha * (x - self._x)`, `self._y += self.alpha * (y - self._y)`.  
5. Return `(self._x, self._y)`.

So the output is always the smoothed position; the internal state is updated for the next frame.

### Optional Kalman filter

When `use_kalman=True`, the tracker uses a 2D constant-velocity Kalman filter instead of EMA. State is `[x, y, vx, vy]`; measurement is `[x, y]`. Predict step: position += velocity; update step: standard Kalman update with the observed (x, y). The same public API applies: `update(x, y)` returns the filtered (x, y); `reset()` clears state so the next sample is treated as new. The main app passes `use_kalman=config.get("use_kalman", False)` when constructing the tracker.

### Method: `reset(self)`

**Inputs:** None.  
**Outputs:** None.  
**Logic:** Set `self._x = self._y = None` (and Kalman state/P to None when use_kalman). Next `update` will treat the next (x, y) as a new first sample. The main app calls `reset()` when the detector returns None (pointer lost).

---

## Calibration: `solve_homography(src_pts, dst_pts)`

**Module:** `smartpi.vision.calibrate`

**Purpose:** Compute a 3×3 homography matrix that maps source (camera) points to destination (projector) points.

**Inputs:**  
- `src_pts`: list of at least 4 (x, y) tuples in camera space.  
- `dst_pts`: list of same length of (x, y) in projector space, same order as src_pts.

**Outputs:** 3×3 NumPy array of dtype float64, or None if fewer than 4 point pairs or if `cv2.findHomography` fails (e.g. degenerate configuration).

**Logic:** If `len(src_pts) < 4` or `len(dst_pts) < 4`, return None. Convert to float32 arrays; call `H, status = cv2.findHomography(src, dst, cv2.RANSAC, 5.0)`. Return H (status is not checked in the current code; RANSAC helps reject outliers). The matrix H maps homogeneous camera coordinates to projector: `[x', y', w']^T = H * [x, y, 1]^T`; pixel coords are `(x'/w', y'/w')`.

---

## Calibration: `save_calibration(path, homography, bounds, resolution)`

**Purpose:** Write calibration to a YAML file (do not commit; file is gitignored).

**Inputs:**  
- `path`: str or Path to output file.  
- `homography`: 3×3 NumPy array.  
- `bounds`: tuple (x0, y0, x1, y1) projector pixel bounds.  
- `resolution`: tuple (width, height) of projector at calibration time.

**Outputs:** None. Creates parent directories if needed; overwrites the file.

**Logic:** Serialize homography with `.tolist()`, bounds and resolution as lists; write with `yaml.safe_dump` (no custom flow style). The file is human-readable YAML.

---

## Calibration: `load_calibration(path) -> dict | None`

**Purpose:** Load calibration from YAML for use at runtime.

**Inputs:** `path`: str or Path to calibration file.

**Outputs:** Dict with keys `homography` (3×3 NumPy float64), `bounds` (list of 4 ints), `resolution` (list of 2 ints), or None if file does not exist or does not contain `homography`.

**Logic:** If path does not exist, return None. Load YAML; if empty or missing "homography", return None. Convert the loaded homography list to a NumPy array (float64). Return the dict.

---

## Calibration: `apply_homography(H, x, y) -> tuple[float, float]`

**Purpose:** Map one camera-space point (x, y) to projector-space pixel coordinates.

**Inputs:** H (3×3), x (float), y (float) in camera pixels.

**Outputs:** (px, py) as two floats in projector pixels.

**Logic:** Form point `pt = np.array([[x, y]], dtype=np.float32)`, reshape to (1, 1, 2) for `cv2.perspectiveTransform`. Call `out = cv2.perspectiveTransform(...)`. Return `(out[0,0,0], out[0,0,1])`.

---

## Validation: `reprojection_error(calibration_path, src_pts, dst_pts) -> float | None`

**Module:** `smartpi.vision.validate`

**Purpose:** Compute median reprojection error in pixels for a set of camera points and expected projector points (e.g. after calibration or for a validation step).

**Inputs:**  
- `calibration_path`: path to calibration.yaml.  
- `src_pts`: list of camera-space (x, y).  
- `dst_pts`: list of expected projector-space (x, y), same order and length.

**Outputs:** Median error in pixels (float), or None if calibration missing/invalid or length mismatch.

**Logic:** Load calibration; if missing or lengths differ, return None. For each (src, dst) pair, compute `(px, py) = apply_homography(H, src[0], src[1])`, then error = hypot(px - dst[0], py - dst[1]). Return `np.median(errors)`.

---

## Data flow summary

- **Wizard:** User taps four corners → wizard collects 4 camera points → `solve_homography(src_pts, DST_PTS)` → `save_calibration(...)`. Optional: validation step collects more points and calls `reprojection_error` to show median error.  
- **Main app at startup:** `load_calibration(config_dir / "calibration.yaml")` → store dict (or None).  
- **Main app per frame:** After detection, if calibration exists: `(px, py) = apply_homography(cal["homography"], cx, cy)`; then `tracker.update(px, py)`; pointer to event layer is in projector space.

So the **order** is: Detect (camera x,y) → Apply homography → Track (projector x,y) → Interact. Calibration (solve/save/load) is one-time; apply is per-frame.

Last updated: 2026-03-04
