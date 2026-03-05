# System Architecture

High-level pipelines and data flow. Diagram sources: [diagrams/architecture.mmd](diagrams/architecture.mmd), [diagrams/calibration_flow.mmd](diagrams/calibration_flow.mmd).

## Pipelines

*Motion to input:* The Pi Camera or Wii Remote tracks the IR pen dot; OpenCV thresholding isolates the dot; **4-point auto-calibration** maps camera FOV to projector display; motion becomes **OS-level mouse events** (draw, click, drag) on the **Kiosk web UI** (plugin scene loaders).

1. **Capture** — Pi Camera or Wii Remote; camera frames (libcamera or OpenCV) at target resolution and FPS.
2. **Detect** — Bright point or IR blob detection → candidate (x, y) in camera space.
3. **Track** — Temporal smoothing (EMA) and optional Kalman; single-pointer first.
4. **Calibrate** — **4-point auto-calibration** (homography) maps camera to projector; persist to `configs/calibration.yaml`.
5. **Interact** — Projector-space coordinates → OS-level mouse events and `PointerEvent` (tap, drag, long-press); adapters (Pygame, WebSocket, uinput).
6. **Render** — Fullscreen display and **Kiosk web UI**; scene selector for Sandbox Draw, Particle Field, plugin scenes, etc.
7. **Operate** — Launcher with health checks, FPS overlay, and fast “recalibrate” flow.

## Why this split

- Swap detectors (IR vs bright point) without changing UI or renderer.
- Swap renderers (Pygame, web, Godot) without changing calibration or tracking.
- Ship a minimal demo quickly, then harden each layer.

## Config reference

- **configs/app.yaml** — Camera index, resolution, detection thresholds (e.g. IR/bright threshold), profile name.
- **configs/calibration.yaml** — Produced by calibration; homography matrix and surface bounds. Do not commit; use `configs/calibration.yaml.example` as schema.
- **configs/profiles/classroom.yaml, dark_room.yaml, daylight.yaml** — Tuning presets (thresholds, exposure hints) for different lighting.
- **configs/logging.yaml** — Log levels and output.
- Optional **app.yaml** keys: `use_libcamera` (Picamera2), `use_kalman` (tracking), `projector_profile` (display size when no calibration). See [config_reference](config_reference.md).

See also [05_calibration_ux.md](05_calibration_ux.md) and [06_interaction_design.md](06_interaction_design.md).

**Full logic and data in/out:** For every function and data boundary in the pipeline, see the [Technical deep dives](technical/README.md) (capture, detect, track, calibrate, interact, render, CLI and operations).

Last updated: 2026-03-04
