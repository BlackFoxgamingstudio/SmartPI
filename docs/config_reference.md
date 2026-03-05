# Config Reference

Purpose and defaults for configuration files. See [04_system_architecture.md](04_system_architecture.md) for pipeline context.

## configs/app.yaml

| Key | Purpose | Default / example |
|-----|----------|-------------------|
| camera_index | Which camera device (0, 1, …) | 0 |
| resolution | Capture width and height in pixels; list `[width, height]` or dict with width/height | e.g. [640, 480] |
| detector | "ir" or "bright" | "bright" |
| threshold | Pixel intensity (0–255) above which a point is treated as the pointer; higher = stricter | From profile |
| profile | Name of profile from configs/profiles/ | "classroom" |
| use_libcamera | If true, use Picamera2 for capture (Pi with libcamera). Requires picamera2 (not in requirements.txt; install on Pi when using libcamera). | false |
| use_kalman | If true, use Kalman filter for pointer smoothing instead of EMA. | false |
| projector_profile | Optional. Name of file in hardware/projector_profiles/ (e.g. generic_1080p) for display size when no calibration. | — |

## configs/calibration.yaml

**Do not commit.** Produced by the calibration wizard.

- **homography** — 3×3 matrix (list of 9 floats, row-major) mapping camera to projector space.
- **bounds** — Optional surface bounds: (x0, y0, x1, y1) in projector pixels for the active projection area.
- **resolution** — Projector resolution (width, height) at calibration time.

Schema example: [configs/calibration.yaml.example](../configs/calibration.yaml.example).

## configs/profiles/*.yaml

Lighting presets (e.g. classroom, dark_room, daylight). Each can override:

- **threshold** — Detection threshold (0–255); see app.yaml.
- **exposure** — Camera exposure hint if supported.
- **blur** — Gaussian blur kernel size (odd integer, in pixels) applied before detection; 0 = no blur. Larger values reduce noise but can soften small pointers.

## configs/logging.yaml

- **level** — DEBUG, INFO, WARNING, ERROR.
- **file** — Optional log file path.

## hardware/projector_profiles/ (optional)

If `app.yaml` includes **projector_profile: <name>** (e.g. `generic_1080p`), the app loads `hardware/projector_profiles/<name>.yaml` when no calibration is present and uses its `resolution` for the display size. Otherwise these files are reference-only:

- **generic_1080p.yaml** — 1920×1080, 60 Hz hint.
- **your_projector_model.yaml** — Template for your model (resolution, refresh_hint).

Use them when documenting your setup or when adding app support for projector-specific config later. Main app config is in `configs/app.yaml` and `configs/profiles/`.

## Ports and URLs

**Default:** This application does not expose any network ports. All interaction is local (display + camera).

If a WebSocket or HTTP server is added later (e.g. for the WebSocket adapter), the port and base URL will be documented here and in the README.

Last updated: 2026-03-04
