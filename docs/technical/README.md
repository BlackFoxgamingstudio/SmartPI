# Technical Deep Dives: Logic and Data In/Out

This folder contains detailed technical documentation that expands on the high-level docs ([00_overview](../00_overview.md), [04_system_architecture](../04_system_architecture.md), [api_overview](../api_overview.md), etc.). Each document explains **all logic and all data in and out** for every function and part of the system, in **order of services and functionality**, with **complete data input and output** through the full pipeline.

## Documents (in pipeline order)

| Doc | Scope | Contents |
|-----|--------|----------|
| [01_system_data_flow_and_services](01_system_data_flow_and_services.md) | End-to-end | Order of services (config → capture → detect → track → calibrate → interact → render → operate); data at each boundary; summary table. |
| [02_capture_layer](02_capture_layer.md) | Capture | `CameraCapture`: constructor, `open()`, `read()`, `release()`, context manager; inputs/outputs and failure modes. |
| [03_vision_preprocess_and_detection](03_vision_preprocess_and_detection.md) | Preprocess + detect | `preprocess_grayscale`, `threshold_mask`; `detect_ir_blob`, `detect_bright_point`; logic and data types. |
| [04_tracking_and_calibration](04_tracking_and_calibration.md) | Track + calibrate | `SmoothingTracker` (update, reset); `solve_homography`, `save_calibration`, `load_calibration`, `apply_homography`; `reprojection_error`. |
| [05_interaction_events_gestures_adapters](05_interaction_events_gestures_adapters.md) | Interaction | `PointerEvent`, `PointerState`; `emit_events_from_track`; `classify_gesture`; Pygame/WebSocket/uinput adapters. |
| [06_renderer_and_ui](06_renderer_and_ui.md) | Renderer + UI | `run_app` loop; scenes (SandboxDraw, ParticleField, StemWidgets); `draw_overlay`; calibration wizard flow. |
| [07_cli_config_and_operations](07_cli_config_and_operations.md) | CLI + operations | `_load_app_config`; commands run, calibrate, healthcheck, export-diagnostics; `get_system_info`, `bundle_diagnostics`. |

## How to use these

- **Implementers:** Use the docs to trace any datum from camera frame to display or to calibration file; each function’s inputs and outputs are spelled out.
- **Maintainers:** When changing a stage (e.g. add a new detector), update the corresponding technical doc and the system data flow doc (01) if boundaries change.
- **Integrators:** The data-flow doc (01) and the summary tables at the end of each doc define the contracts between layers.

These technical docs satisfy the requirement that every bullet point (every function and part of the system) be explained with full logic and complete data input and output, in order of services and functionality across the full system.

Last updated: 2025-03-04
