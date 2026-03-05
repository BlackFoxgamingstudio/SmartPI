# Capture Layer: Logic and Data In/Out

This document describes the capture layer of Smart Pi in full detail: every function, every input and output, the logic used, and how it fits into the system. The capture layer is the first pipeline stage and is the only source of image data for detection and (in the calibration wizard) for visual feedback.

## Role of the capture layer

The capture layer abstracts the camera hardware behind a simple interface: open the device with a given resolution and frame rate, read frames one at a time as BGR NumPy arrays, and release the device when done. No detection, no drawing—only acquisition. All configuration (camera index, width, height, FPS) comes from the application or calibration config, not from the capture class itself. This keeps the pipeline testable: tests can inject frames without a real camera by mocking or replacing the capture instance.

## Module and public API

**Module:** `smartpi.core.capture`  
**Public factory:** `create_capture(camera_index, width, height, fps, use_libcamera=False)` — returns a capture instance (see “Optional libcamera path” below).  
**Public classes:** `CameraCapture`, `LibcameraCapture`  
**Public methods (both classes):** `open()`, `read()`, `release()`, and context manager support (`__enter__` / `__exit__`). `CameraCapture` also has `__init__(camera_index, width, height, fps)`.

The main app uses `create_capture(..., config.get("use_libcamera", False))` so that when `use_libcamera` is True and the `picamera2` package is available (e.g. on Raspberry Pi), it gets a `LibcameraCapture` instance; otherwise it gets `CameraCapture` (OpenCV). Both implement the same interface.

## Optional libcamera path

**Factory: `create_capture(camera_index, width, height, fps, use_libcamera=False)`**

**Purpose:** Return a capture instance. When `use_libcamera` is True, the implementation tries to import `picamera2` and returns a `LibcameraCapture(width, height, fps)` (camera_index is ignored for libcamera). When `use_libcamera` is False or the import fails, returns `CameraCapture(camera_index, width, height, fps)`.

**Inputs:** `camera_index` (int), `width`, `height` (int), `fps` (float), `use_libcamera` (bool).  
**Outputs:** An instance of `LibcameraCapture` or `CameraCapture` with the same interface: `open()`, `read()`, `release()`.

**LibcameraCapture:** Uses the Picamera2 API (libcamera on Raspberry Pi). Same contract as CameraCapture: `open()` returns True if the camera was configured and started (BGR888, requested size); `read()` returns `(True, frame)` with frame a BGR NumPy array, or `(False, None)` on failure; `release()` stops the camera. Requires the `picamera2` package (not in requirements.txt; install on Pi when using libcamera).

## Constructor: `__init__(camera_index, width, height, fps)`

**Purpose:** Store the parameters that will be used when the camera is opened. No device is opened at construction time; this allows creating the object before deciding whether to use it (e.g. in tests or conditional branches).

**Inputs:**

- `camera_index` (int): OpenCV camera device index. On Linux this is typically 0 for `/dev/video0`, 1 for `/dev/video1`, etc. Must be a non-negative integer that the system recognizes as a video capture device.
- `width` (int): Desired frame width in pixels. Passed to OpenCV as `CAP_PROP_FRAME_WIDTH`. Common values: 640, 1280, 1920.
- `height` (int): Desired frame height in pixels. Passed as `CAP_PROP_FRAME_HEIGHT`. Common values: 480, 720, 1080.
- `fps` (float): Target frames per second. Passed as `CAP_PROP_FPS`. The driver may not achieve this exactly; the actual rate can be observed via timing (e.g. `FPSCounter` in the main app).

**Outputs:** None. The object is initialized with these values stored and `self._cap` set to `None` (no device opened yet).

**Logic:** Assign the four parameters to instance attributes with the same names. Set `self._cap = None`. No validation is performed (e.g. no check that camera_index exists); validation effectively happens when `open()` is called.

**Usage:** The main app and the calibration wizard obtain camera_index, width, and height from config (and use a default FPS such as 30.0). They construct one `CameraCapture` and then call `open()` before the main loop.

## Method: `open()`

**Purpose:** Open the camera device and set its resolution and FPS. Must be called before `read()`.

**Inputs:** None (uses `self.camera_index`, `self.width`, `self.height`, `self.fps` from construction).

**Outputs:** `bool`. `True` if the device was opened and properties were set; `False` if `cv2.VideoCapture(self.camera_index)` failed to open (e.g. device in use, wrong index, or no permission).

**Logic:** (1) Create `self._cap = cv2.VideoCapture(self.camera_index)`. (2) If `not self._cap.isOpened()`, return `False` (and leave `_cap` as the failed object—caller typically checks the return value and does not call `read()`). (3) Call `self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)`, then same for `CAP_PROP_FRAME_HEIGHT` and `CAP_PROP_FPS`. (4) Return `True`. OpenCV does not guarantee that the requested resolution is applied; the driver may choose the nearest supported mode. The next `read()` will return frames at whatever resolution the device actually provides.

**Usage:** The main app does `capture.open()` and raises `RuntimeError("Could not open camera")` if it returns False, then enters the main loop. The calibration wizard does the same. Callers must not call `open()` twice without an intervening `release()`; behavior with a second `open()` is undefined (may leak a handle or replace the previous one).

## Method: `read()`

**Purpose:** Read one frame from the camera. This is the only method that returns image data and is the sole output of the capture layer for the rest of the pipeline.

**Inputs:** None.

**Outputs:** `tuple[bool, np.ndarray | None]`. First element: success flag. Second element: if success is True, a NumPy array of shape `(height, width, 3)` in BGR order, dtype typically `uint8`; if success is False, `None`. The dimensions of the array may not exactly match the requested width/height if the driver rounded to a different resolution.

**Logic:** (1) If `self._cap is None` or `not self._cap.isOpened()`, return `(False, None)`. (2) Call `ret, frame = self._cap.read()`. (3) If `not ret or frame is None`, return `(False, None)`. (4) Return `(True, frame)`. So any failure path yields `(False, None)`; the caller can treat “no frame” uniformly (e.g. skip detection, draw a fallback, and continue the loop).

**Usage:** The main loop calls `ret, frame = capture.read()` once per iteration. If `not ret or frame is None`, the app does not run the detector; it draws the current scene (or a blank screen) and overlay, flips the display, and ticks the clock at a lower rate (e.g. 10 FPS) to avoid busy-waiting. When the camera is working, the same frame is passed to the detector (IR or bright) and is not stored beyond that frame.

**Data contract for downstream:** The detector expects `frame` to be either BGR (3 channels) or grayscale (2D). The preprocess step converts BGR to grayscale if needed, so the capture layer does not need to convert; BGR is the OpenCV default and is what the rest of the vision pipeline expects.

## Method: `release()`

**Purpose:** Release the camera device so other processes can use it and resources are freed.

**Inputs:** None.

**Outputs:** None.

**Logic:** If `self._cap is not None`, call `self._cap.release()` and set `self._cap = None`. Idempotent: calling `release()` again has no effect.

**Usage:** The main app calls `capture.release()` in a `finally` block after the main loop (and then `pygame.quit()`). The calibration wizard releases the capture when the wizard exits. If the process is killed without a clean exit, the OS will eventually release the device, but it is good practice to always call `release()` on the normal path.

## Context manager: `__enter__` and `__exit__`

**Purpose:** Allow using `with CameraCapture(...) as cap:` so that `open()` is called on entry and `release()` is called on exit (including on exception).

**Inputs:** `__enter__` takes no arguments beyond `self`. `__exit__(self, *args)` receives the standard three exception arguments (exc_type, exc_val, exc_tb).

**Outputs:** `__enter__` returns `self` after calling `self.open()` (it does not check the return value of `open()`; the caller may check by testing a subsequent `read()`). `__exit__` returns None (exceptions are not suppressed).

**Logic:** `__enter__`: call `self.open()`, return `self`. `__exit__`: call `self.release()`, ignore `*args`. So the context manager does not raise if `open()` fails; the user must check after `with ... as cap:` whether `cap.read()` works.

## Integration with config

The capture layer does not read config files. The **caller** (main app or calibration wizard) loads config and passes in:

- `camera_index`: from `config.get("camera_index", 0)`
- `width`, `height`: from `config.get("resolution", [640, 480])` (first and second element)
- `fps`: often hardcoded (e.g. 30.0) in the app; could be added to config later
- `use_libcamera`: from `config.get("use_libcamera", False)`; when True, the app uses `create_capture(..., use_libcamera=True)` to obtain a LibcameraCapture when available.

So the data flow is: **Config (YAML) → app/wizard → create_capture(...) or CameraCapture(__init__ + open)**. The capture layer’s only input from the rest of the system is the parameters it receives at construction and the implicit call order (open before read, release at end).

## Failure modes and edge cases

- **Camera already in use:** `open()` may succeed or fail depending on the driver; if it fails, `isOpened()` is False and the app should exit or show an error.
- **Resolution not supported:** OpenCV may set a different resolution; the returned frame size may differ from the requested size. Detectors and homography assume a consistent resolution; if the driver changes resolution mid-stream, behavior is undefined. In practice, once opened, the resolution is usually stable.
- **Read fails occasionally:** e.g. USB bandwidth or driver glitch. `read()` returns `(False, None)`; the app treats it as “no frame this time” and continues, which avoids crashing on transient errors.
- **No calibration:** The capture layer is unaffected. Calibration only affects the mapping from camera to projector after detection; the capture layer always outputs camera-space frames.

## Summary: data in and out

| Function / use      | Data in                          | Data out                    |
|---------------------|----------------------------------|-----------------------------|
| `__init__`          | camera_index, width, height, fps | (none; object initialized)  |
| `open()`            | (none)                           | bool                        |
| `read()`            | (none)                           | (bool, np.ndarray \| None)   |
| `release()`         | (none)                           | (none)                      |
| `__enter__`         | (none)                           | self                        |
| `__exit__`          | exc_type, exc_val, exc_tb        | None                        |

The capture layer is the single source of raw frames for the entire vision and interaction pipeline. The next document covers preprocessing and detection, which consume this frame and produce the first pointer position (camera-space x, y).

Last updated: 2026-03-04
