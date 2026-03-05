# API Overview

High-level reference for the Smart Pi public API. The pipeline translates **motion to input**: Capture (Pi Camera or Wii Remote, IR pen dot) → Process (OpenCV thresholding, 4-point auto-calibration) → Interact (OS-level mouse events on the Kiosk web UI). See [04_system_architecture.md](04_system_architecture.md).

**Public API:** Symbols listed below (modules, classes, and functions without a leading `_`) in `smartpi.*` are the supported public surface. Names starting with `_` (e.g. `_load_config`) are internal and may change without notice. Prefer the public entry points (`run_app`, `run_wizard`, CLI commands, and the symbols in the tables).

**Parameters, return values, and errors:** For each function, see the docstrings in `src/smartpi/`. If the source and this overview disagree, the source is the authority; please open an issue to fix the doc.

**Example — key function contracts:**

| Symbol | Parameters | Returns | Errors / notes |
|--------|------------|---------|----------------|
| `detect_ir_blob(frame, threshold, blur_ksize, morph_ksize)` | BGR/gray frame; threshold 0–255; odd kernel sizes | `(cx, cy)` or `None` | Returns `None` if no blob ≥ area threshold |
| `apply_homography(H, x, y)` | 3×3 matrix H, camera (x, y) | `(px, py)` projector pixels | — |
| `load_calibration(path)` | Path to YAML | `dict` with homography, bounds, resolution or `None` | Returns `None` if file missing or invalid |

## CLI

- **Entry point:** `smartpi.cli:main` (script: `smartpi`)
- **Commands:** `run`, `calibrate`, `healthcheck`, `export-diagnostics`, `bom`
- **Config:** Loaded from `configs/app.yaml` and profile (e.g. `configs/profiles/classroom.yaml`). See [config_reference.md](config_reference.md).
- **BOM:** `smartpi bom` prints the main BOM from `hardware/bom.csv`; `smartpi bom --pen` also prints `hardware/ir_pen/pen_bom.csv`. Use `--repo` to point to the repository root.

## Core

| Module | Main symbols | Purpose |
|--------|--------------|---------|
| `smartpi.core.capture` | `CameraCapture`, `LibcameraCapture`, `create_capture` | Camera frame capture (OpenCV or optional Picamera2 when `use_libcamera`). |
| `smartpi.core.projector_profile` | `load_projector_profile` | Load `hardware/projector_profiles/<name>.yaml` (resolution, refresh_hint). |
| `smartpi.core.timing` | `FPSCounter` | FPS measurement. |
| `smartpi.core.diagnostics` | `get_system_info`, `bundle_diagnostics` | System info and diagnostic bundle for bug reports. |
| `smartpi.core.bom` | `load_bom`, `load_main_bom`, `load_pen_bom` | Load BOM CSV files (stdlib `csv`). See below. |

**BOM (CSV):** The app does not load BOM at runtime for projection; the CSVs are for replication and tooling. Use `load_bom(path)` for any CSV (returns `list[dict]` with header keys); `load_main_bom(repo_root)` and `load_pen_bom(repo_root)` resolve `hardware/bom.csv` and `hardware/ir_pen/pen_bom.csv` relative to `repo_root`. Raises `FileNotFoundError` if the file is missing.

## Vision

| Module | Main symbols | Purpose |
|--------|--------------|---------|
| `smartpi.vision.preprocess` | `preprocess_grayscale`, `threshold_mask` | Grayscale and threshold preprocessing. |
| `smartpi.vision.detect_ir` | `detect_ir_blob` | IR blob detection (camera-space point). |
| `smartpi.vision.detect_bright` | `detect_bright_point` | Bright-point detection (camera-space). |
| `smartpi.vision.track` | `SmoothingTracker` | Temporal smoothing (EMA or optional Kalman when use_kalman) of pointer position. |
| `smartpi.vision.calibrate` | `solve_homography`, `save_calibration`, `load_calibration`, `apply_homography` | 4-point homography and calibration I/O. |
| `smartpi.vision.validate` | `reprojection_error` | Validation error (e.g. after calibration). |

## Interaction

| Module | Main symbols | Purpose |
|--------|--------------|---------|
| `smartpi.interaction.events` | `PointerState`, `PointerEvent` | Pointer event model (x, y, state, timestamp). |
| `smartpi.interaction.gesture` | `classify_gesture`, `emit_events_from_track` | Gesture classification and event emission from track. |
| `smartpi.interaction.adapters.pygame_adapter` | `pygame_event_from_pointer`, `push_to_pygame` | Map `PointerEvent` to Pygame events. |
| `smartpi.interaction.adapters.websocket_adapter` | `send_pointer_event` | Send pointer events over WebSocket. |
| `smartpi.interaction.adapters.uinput_adapter` | `emit_mouse` | Emit mouse events via uinput (Linux). |

## Renderer

| Module | Main symbols | Purpose |
|--------|--------------|---------|
| `smartpi.renderer.pygame_app` | `run_app` | Main Pygame app loop; scene selector, homography. |
| `smartpi.renderer.scenes.sandbox_draw` | `SandboxDrawScene` | Drawing scene. |
| `smartpi.renderer.scenes.particle_field` | `ParticleFieldScene` | Particle field scene. |
| `smartpi.renderer.scenes.stem_widgets` | `StemWidgetsScene` | STEM widgets scene. |

## UI

| Module | Main symbols | Purpose |
|--------|--------------|---------|
| `smartpi.ui.calibration_wizard` | `run_wizard` | 4-corner calibration wizard (Pygame or OpenCV). |
| `smartpi.ui.overlay` | `draw_overlay` | Draw FPS/overlay on frame. |

## Generating full API docs

To build HTML API docs from docstrings (optional), you can use:

- **Sphinx:** `sphinx-quickstart` in `docs/`, then configure `autodoc` and `sphinx-apidoc -o docs/api src/smartpi`.
- **MkDocs + mkdocstrings:** Add `mkdocstrings` and reference `smartpi` in a MkDocs page.

**Detailed logic and data flow:** For full inputs, outputs, and logic of every function and part of the system in pipeline order, see the [Technical deep dives](technical/README.md).

Last updated: 2026-03-04
