# Overview

**Smart Pi Projector** (Smart Pi) is a repair-forward, portable interactive projection system for **creative collaboration and STEM learning**—*upcycling e-waste into interactive, open-source classrooms*. It turns a Raspberry Pi, a projector, and a camera into an interactive display: **any flat wall becomes a touchscreen whiteboard** via IR tracking and a Raspberry Pi. A pointer (IR pen or bright spot) is detected by the camera, mapped to projector coordinates via 4-point calibration, and used to drive visuals on the **Kiosk web UI** (drawing, particles, plugin scene loaders).

**Vision:** *Transform passive consumption into active creation*—from planned obsolescence to planned repair.

## Who is this for

- **Educators & districts:** Cost-disruptive alternative to traditional EdTech (~$215 per Starter Kit; 10 rooms for ~$2,150 vs $20,000). **25-kit R&D Pilot Program** for classrooms. See [11_problem_and_value.md](11_problem_and_value.md).
- **Makers & developers:** Open-source community; [GitHub](https://github.com/SmartPiProjector) and docs; [CONTRIBUTING.md](../CONTRIBUTING.md).
- **Recyclers & surplus:** Partner for local supply MOUs and e-waste diversion. See [03_repair_forward_notes.md](03_repair_forward_notes.md).
- **Hackathon / demo:** Get a working “touch-like” projection in a weekend.
- **Workshops / classrooms:** Replicable setup with a clear build guide and BOM. **STEM by Design:** Students assemble hardware, learn optics, flash OS, perform maintenance; kit as curriculum (repair literacy, technical confidence).
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

## Ways to contribute

1. **Hardware rigging** — Mounts, cabling, transport, portable demo rig.
2. **Interaction design** — Gestures, adapters, calibration UX.
3. **Creative visuals and sound** — New scenes, audio, collaboration tools.
4. **Fast calibration UX** — Fewer steps, reliability, quick recalibrate.

See [CONTRIBUTING.md](../CONTRIBUTING.md) and the role-based map in the repo. The project adopts a **quarterly release cadence**, **clear plugin APIs**, and welcomes **open-source university contributors** (e.g. CS/EE capstone).

## Broader impact (ESG)

- **E-waste diversion** — Keep heavy projectors, lamps, and filters in active service (target: 7,500+ lbs diverted).
- **Cost savings** — Capital reallocated from proprietary tech to student programs (target: $250k+ saved).
- **Student skill development** — Tangible repair hours in electronics, Linux, and optics (target: 4,000+ student repair hours logged).

*A transition from planned obsolescence to planned repair.*

Last updated: 2026-03-04
