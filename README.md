# Smart Pi Interactive Projection

[![CI](https://github.com/YOUR_ORG/rashbarrypi/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_ORG/rashbarrypi/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/YOUR_ORG/rashbarrypi/graph/badge.svg)](https://codecov.io/gh/YOUR_ORG/rashbarrypi)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Before publishing:** Replace `YOUR_ORG` (and `YOUR_GITHUB_USERNAME` in [CODEOWNERS](.github/CODEOWNERS)) in this README, [CONTRIBUTING.md](CONTRIBUTING.md), and [CITATION.cff](CITATION.cff) with your GitHub org/user and repo details.

Camera-based interactive projection on Raspberry Pi: use an IR pen or bright pointer to draw and interact with projected visuals. Designed for hackathon demos, workshops, and replicable installations.

## Table of contents

- [Who maintains this](#who-maintains-this)
- [Why this project exists](#why-this-project-exists)
- [What it does](#what-it-does)
- [Requirements](#requirements)
- [Get started](#get-started)
- [Documentation](#documentation)
- [Scope](#scope)
- [Known issues and support](#known-issues-and-support)
- [Changelog and contributing](#changelog-and-contributing)
- [Version](#version)
- [License](#license)

## Who maintains this

Smart Pi is maintained by the community. See [MAINTAINERS.md](MAINTAINERS.md) and [CONTRIBUTING.md](CONTRIBUTING.md) for how to contribute and get help.

## Why this project exists

Surplus projectors and a Pi can become an interactive wall or table without touch hardware. This project provides the full pipeline: capture camera frames, detect a pointer (IR pen or laser/bright spot), calibrate camera-to-projector mapping, and drive Pygame (or other) visuals. You get a working demo and a structure others can extend.

## What it does

- **Capture** — Camera frames via libcamera/OpenCV  
- **Detect** — IR blob or visible bright-point detection  
- **Track** — Single-pointer smoothing (EMA, optional Kalman)  
- **Calibrate** — 4-point homography, persist to config  
- **Interact** — Pointer events (tap, drag, long-press) and adapters (Pygame, WebSocket)  
- **Render** — Sandbox Draw, Particle Field, and STEM Widgets (ruler, angles, graph paper) demo scenes  
- **Operate** — Kiosk launcher, healthcheck, recalibrate flow  

## Requirements

- **Hardware:** Raspberry Pi 4/5 (recommended), HDMI projector, camera (USB or CSI). For IR mode: IR pen and optionally IR-pass filter.
- **OS:** Raspberry Pi OS (or compatible Linux).
- **Software:** Python 3.10+, OpenCV, Pygame, NumPy, PyYAML. See [docs/02_build_guide.md](docs/02_build_guide.md) and [docs/01_bill_of_materials.md](docs/01_bill_of_materials.md).

## Get started

```bash
git clone https://github.com/YOUR_ORG/rashbarrypi.git
cd rashbarrypi
make install
# On Pi: connect camera and projector, then:
make run
```

For a full setup (Pi, projector, camera, calibration), follow the [Build guide](docs/02_build_guide.md) and use the [Bill of materials](docs/01_bill_of_materials.md) (BOM).

**Quick run (no hardware):** `make run` starts the app; without a camera or calibration, you may see only the overlay or a placeholder.

**Check setup and calibrate (with hardware):**
```bash
smartpi healthcheck
smartpi calibrate
smartpi run
```

## Documentation

| Doc | Description |
|-----|-------------|
| [00_overview](docs/00_overview.md) | Overview and where to start |
| [01_bill_of_materials](docs/01_bill_of_materials.md) | Parts list (projector, camera, IR pen, mounts) |
| [02_build_guide](docs/02_build_guide.md) | Step-by-step setup to “demo running” |
| [03_repair_forward_notes](docs/03_repair_forward_notes.md) | Repair, surplus sourcing, longevity |
| [04_system_architecture](docs/04_system_architecture.md) | Pipelines and data flow |
| [05_calibration_ux](docs/05_calibration_ux.md) | Calibration steps and troubleshooting |
| [06_interaction_design](docs/06_interaction_design.md) | PointerEvent, gestures, adapters |
| [07_troubleshooting](docs/07_troubleshooting.md) | No camera, low FPS, bad alignment, lighting |
| [08_safety_and_power](docs/08_safety_and_power.md) | Safety and power considerations |
| [09_accessibility_and_inclusion](docs/09_accessibility_and_inclusion.md) | Accessibility and inclusion |
| [config_reference](docs/config_reference.md) | Config options and defaults |
| [Diagrams](docs/diagrams/README.md) | Architecture and calibration flow (Mermaid) |
| [Demo walkthrough](docs/demo_walkthrough/) | Showcase script, operator checklist |
| [00_best_practices](docs/00_best_practices.md) | Open source best practices checklist |
| [API overview](docs/api_overview.md) | Public API and docstrings reference |

## Scope

- **In scope:** Raspberry Pi (4/5 recommended), Linux (Raspberry Pi OS or compatible), camera-based pointer tracking (IR pen or bright spot), homography calibration, Pygame demo scenes, kiosk-style operation, BOM and build guide for replication.
- **Out of scope:** Windows/macOS host support; official pre-built hardware kits; guaranteed real-time performance for safety-critical use; commercial support or SLAs.

## Known issues and support

- **Known issues:** See [ROADMAP.md](ROADMAP.md) and [docs/07_troubleshooting.md](docs/07_troubleshooting.md). Report bugs via [GitHub Issues](https://github.com/YOUR_ORG/rashbarrypi/issues) using the bug report template.
- **Support level:** Community, best-effort. We aim to triage issues within a few days (see [CONTRIBUTING.md](CONTRIBUTING.md)).

## Changelog and contributing

- [CHANGELOG.md](CHANGELOG.md) — Release history  
- [CONTRIBUTING.md](CONTRIBUTING.md) — How to contribute, code style, PR process  
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) — Community standards  

## Version

Latest stable: **v0.1.0** (see [CHANGELOG.md](CHANGELOG.md) and [ROADMAP.md](ROADMAP.md)). The single source of truth for the version is `pyproject.toml`; CITATION.cff and this README should be updated when cutting a release (see [CONTRIBUTING.md](CONTRIBUTING.md)#versioning-and-releases).

## License

MIT. See [LICENSE](LICENSE).
