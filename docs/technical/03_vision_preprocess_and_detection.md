# Vision: Preprocess and Detection — Logic and Data In/Out

This document covers the preprocessing and detection stages of the Smart Pi vision pipeline. Every function’s inputs, outputs, and internal logic are specified so that data flow from a raw camera frame to a single camera-space (x, y) point (or None) is fully traceable.

## Role of preprocessing and detection

After the capture layer provides a BGR frame, the pipeline must decide “where is the pointer?” in that frame. The pointer is either an IR blob (IR pen tip) or the brightest spot (laser or LED). Preprocessing converts the frame to a form suitable for thresholding and blob/peak finding; detection then produces one point or None. All coordinates in this stage are in **camera image space** (origin top-left, x right, y down, units pixels). Homography to projector space is applied later.

## Module layout

- **smartpi.vision.preprocess:** `preprocess_grayscale(frame, blur_ksize)`, `threshold_mask(gray, threshold)`
- **smartpi.vision.detect_ir:** `detect_ir_blob(frame, threshold, blur_ksize, morph_ksize)`
- **smartpi.vision.detect_bright:** `detect_bright_point(frame, threshold, blur_ksize)`

The IR detector uses both preprocess functions and adds morphology and contour analysis. The bright-point detector uses only `preprocess_grayscale` and then OpenCV’s `minMaxLoc`. Both return `tuple[float, float] | None`.

---

## Preprocess: `preprocess_grayscale(frame, blur_ksize)`

**Purpose:** Convert the input frame to grayscale and optionally apply a Gaussian blur to reduce noise before thresholding or peak detection.

**Inputs:**

- `frame` (np.ndarray): BGR image of shape (H, W, 3) or grayscale (H, W). Dtype typically uint8. Comes directly from `CameraCapture.read()`.
- `blur_ksize` (int): Kernel size for Gaussian blur; must be odd and positive to blur, or 0 to skip blur.

**Outputs:** Grayscale image of shape (H, W), dtype uint8. Same dimensions as the input (except if input was BGR, the channel dimension is removed).

**Logic:** (1) If `len(frame.shape) == 3`, convert BGR to grayscale with `cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)`; otherwise take `gray = frame.copy()`. (2) If `blur_ksize > 0` and `blur_ksize % 2 == 1`, call `cv2.GaussianBlur(gray, (blur_ksize, blur_ksize), 0)` and use the result; otherwise leave gray unchanged. (3) Return the grayscale array. Sigma for the Gaussian is 0 (OpenCV computes it from kernel size).

**Data contract:** Downstream (threshold_mask, minMaxLoc, contour finding) expect a single-channel uint8 image. Blur reduces high-frequency noise so that a single bright point or blob is more stable across frames.

---

## Preprocess: `threshold_mask(gray, threshold)`

**Purpose:** Produce a binary mask where every pixel with value >= threshold is 255 and others are 0. Used only by the IR detector to isolate bright (IR) regions before morphology and contours.

**Inputs:**

- `gray` (np.ndarray): Grayscale image (H, W), uint8.
- `threshold` (int): Value in 0–255. Pixels with gray value >= threshold become 255; others become 0.

**Outputs:** Binary image (H, W), uint8, values 0 or 255.

**Logic:** `_, mask = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)`. So it is a single global threshold, not adaptive. Choice of threshold is critical: too low and ambient light creates many regions; too high and the IR pen tip may be missed.

**Usage:** Only `detect_ir_blob` calls this. `detect_bright_point` does not use a mask; it uses the grayscale image and minMaxLoc directly.

---

## Detection: `detect_ir_blob(frame, threshold, blur_ksize, morph_ksize)`

**Purpose:** Find the single largest bright (IR) blob in the frame and return its centroid in camera coordinates, or None if no valid blob is found.

**Inputs:**

- `frame` (np.ndarray): BGR or grayscale from capture.
- `threshold` (int): 0–255; passed to `threshold_mask`.
- `blur_ksize` (int): Odd positive or 0; passed to `preprocess_grayscale`.
- `morph_ksize` (int): Odd positive for morphology kernel size; 0 to skip morphology.

**Outputs:** `tuple[float, float] | None`. If a blob is found: (cx, cy) in pixel coordinates (float). Otherwise None.

**Logic (step by step):**

1. **Grayscale and blur:** `gray = preprocess_grayscale(frame, blur_ksize)`.
2. **Threshold:** `mask = threshold_mask(gray, threshold)`.
3. **Morphology (if morph_ksize > 0 and odd):** Build an elliptical structuring element of size (morph_ksize, morph_ksize). Apply `cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)` to fill small holes, then `cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)` to remove small isolated regions. This cleans the mask so that the IR pen tip is one connected component.
4. **Contours:** `contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)`. Only external contours are kept.
5. **Largest contour:** If contours is empty, return None. Otherwise `largest = max(contours, key=cv2.contourArea)`.
6. **Area filter:** If `cv2.contourArea(largest) < 10`, return None (reject tiny noise blobs).
7. **Centroid:** Compute moments with `cv2.moments(largest)`. If `M["m00"] == 0`, return None. Else `cx = M["m10"]/M["m00"]`, `cy = M["m01"]/M["m00"]`. Return `(float(cx), float(cy))`.

**Data flow:** frame → grayscale+blur → mask → morphology → contours → largest → area check → moments → (cx, cy). So the only output is one 2D point or None; no confidence score or multiple blobs are exposed in the current API.

---

## Detection: `detect_bright_point(frame, threshold, blur_ksize)`

**Purpose:** Find the single brightest pixel in the frame (e.g. laser or LED). Simpler than IR: no contours, no morphology—just grayscale max with a minimum brightness threshold.

**Inputs:**

- `frame` (np.ndarray): BGR from capture.
- `threshold` (int): Minimum gray value for the max to be accepted; if the global max is below this, return None.
- `blur_ksize` (int): Passed to `preprocess_grayscale`; 0 to skip blur.

**Outputs:** `tuple[float, float] | None`. (x, y) of the brightest pixel if its value >= threshold, else None.

**Logic:** (1) `gray = preprocess_grayscale(frame, blur_ksize)`. (2) `min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(gray)`. (3) If `max_val < threshold`, return None. (4) Return `(float(max_loc[0]), float(max_loc[1]))`. So a single pixel location is returned; subpixel refinement is not done in the current implementation.

**Comparison with IR:** Bright-point is faster (no contours or morphology) but more sensitive to noise and specular reflections; IR is more robust when an IR-pass filter is used. Both return the same type: one (x, y) or None.

---

## How the app chooses and calls the detector

The main app (and calibration wizard where applicable) reads config: `detector = config.get("detector", "bright")`, `threshold = config.get("threshold", 200)`, `blur = config.get("blur", 3)`. Then each frame:

- If `detector == "ir"`: `pt = detect_ir_blob(frame, threshold=threshold, blur_ksize=blur)` (morph_ksize often default 5 in code or could be from config).
- Else: `pt = detect_bright_point(frame, threshold=threshold, blur_ksize=blur)`.

So the **input** to the detection stage is: one BGR frame + config (detector type, threshold, blur). The **output** is a single camera-space point or None. That output is the only input to the next stage (after optional homography in the main app: camera point is mapped to projector, then given to the tracker).

---

## Coordinate system and units

All coordinates in preprocess and detection are in **camera image coordinates**: origin at top-left of the image, x increasing right, y increasing down, units in pixels. The point (0, 0) is the top-left pixel; (width-1, height-1) is the bottom-right. Float values are used so that centroids (from moments) can be subpixel. The homography stage later maps these (cx, cy) to projector pixel space; preprocessing and detection do not need to know the projector resolution.

---

## Edge cases and failure modes

- **No pointer in view:** Both detectors return None. The main loop will call `tracker.reset()` and set pointer to None; the event layer may emit an UP event if the pointer was previously down.
- **Multiple bright regions (IR):** The IR detector returns the **largest** contour by area. If two blobs are present, only one point is returned; multi-pointer is a future roadmap item.
- **Ambient light / reflection:** Can create false bright spots. Tuning threshold and blur (and for IR, morphology) reduces this; profile presets (classroom, dark_room, daylight) are intended for different lighting.
- **Frame size mismatch:** Preprocess and detection assume the frame is the same resolution every time. If capture changes resolution mid-run, behavior is undefined.

---

## Summary: data in and out

| Function                 | Data in                                      | Data out              |
|--------------------------|----------------------------------------------|------------------------|
| preprocess_grayscale     | frame (BGR or gray), blur_ksize              | gray (H×W uint8)       |
| threshold_mask           | gray, threshold                             | mask (H×W 0/255)       |
| detect_ir_blob           | frame, threshold, blur_ksize, morph_ksize   | (x,y) or None          |
| detect_bright_point      | frame, threshold, blur_ksize                | (x,y) or None          |

The next document covers tracking (smoothing of the 2D point) and calibration (homography solve, save/load, apply, and validation).

Last updated: 2025-03-04
