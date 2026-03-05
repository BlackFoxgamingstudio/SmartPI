# Overview

Smart Pi Interactive Projection turns a Raspberry Pi, a projector, and a camera into an interactive display. A pointer (IR pen or bright spot) is detected by the camera, mapped to projector coordinates via calibration, and used to drive visuals—drawing, particles, or custom scenes.

## Who is this for

- **Hackathon / demo:** Get a working “touch-like” projection in a weekend.
- **Workshops / classrooms:** Replicable setup with a clear build guide and BOM.
- **Makers:** Extend with new scenes, detectors, or renderers without changing the core pipeline.

## Where to start

1. **Parts and cost** — [01_bill_of_materials.md](01_bill_of_materials.md) and [hardware/bom.csv](../hardware/bom.csv).
2. **Build step-by-step** — [02_build_guide.md](02_build_guide.md) (from zero to “demo running”).
3. **How it works** — [04_system_architecture.md](04_system_architecture.md) (capture → detect → track → calibrate → interact → render).
4. **Calibration** — [05_calibration_ux.md](05_calibration_ux.md).
5. **Problems?** — [07_troubleshooting.md](07_troubleshooting.md).

## Project structure (high level)

- **Config** — `configs/`: app settings, calibration result, lighting profiles. Optional: `projector_profile` (from hardware/projector_profiles/), `use_libcamera`, `use_kalman` (see [config_reference](config_reference.md)). Print BOM: `smartpi bom`.
- **Code** — `src/smartpi/`: core (capture, timing), vision (detect, track, calibrate), interaction (events, gestures), renderer (Pygame scenes), UI (wizard, overlay).
- **Scripts** — `scripts/`: install, healthcheck, calibrate, run_demo, export_diagnostics.
- **Docs** — This folder; diagrams in `docs/diagrams/`.

Last updated: 2026-03-04
