# Bill of Materials (BOM)

**Canonical** here means the authoritative part list for building the Smart Pi setup; replicate from this list for a supported build. For a machine-readable list with part numbers or model IDs, see [hardware/bom.csv](../hardware/bom.csv) (columns: part, part_number_or_model, quantity, supplier, notes). You can print the BOM from the CLI: `smartpi bom` (and `smartpi bom --pen` for the IR pen BOM). The Python API is in `smartpi.core.bom`: `load_bom(path)`, `load_main_bom(repo_root)`, `load_pen_bom(repo_root)` — see [api_overview.md](api_overview.md).

## Compute and display

| Item | Notes |
|------|--------|
| Raspberry Pi 4 or 5 | Pi 4/5 recommended for OpenCV; Pi Zero can play content but is slow for vision. |
| HDMI projector | 720p or 1080p; surplus/used is fine. See [03_repair_forward_notes.md](03_repair_forward_notes.md). |
| MicroSD card | 16 GB+ for Pi OS and dependencies. |
| Power supply | Official Pi PSU or equivalent (5 V, sufficient current). |

## Camera and pointer

**Option A — IR pen (recommended for robustness)**  
*Robustness*: IR mode is less affected by ambient visible light than bright-point mode, so detection is more stable in varying room lighting.

| Item | Notes |
|------|--------|
| IR-sensitive camera | USB or CSI; no IR filter or with IR-pass filter. |
| IR pen | LED at tip; compatible with camera’s sensitivity. |
| (Optional) IR-pass / visible-cut filter | Reduces ambient visible light for cleaner detection. |

**Option B — Visible bright point (simplest)**

| Item | Notes |
|------|--------|
| Webcam or Pi camera | Standard USB or CSI. |
| Laser pointer or bright LED | Used as the “pointer” on the surface. |

## Mounts and enclosure

- **Camera mount** — Positions the camera so it sees the full projected area with minimal occlusion (no part of the projection surface blocked from the camera’s view). See [hardware/camera_mount/](../hardware/camera_mount/).
- **IR pen** — Build or buy; BOM in [hardware/ir_pen/pen_bom.csv](../hardware/ir_pen/pen_bom.csv), [hardware/ir_pen/README.md](../hardware/ir_pen/README.md).
- **Enclosure** — Optional; see [hardware/enclosure/](../hardware/enclosure/).

## Cables and misc

- HDMI cable (Pi → projector).
- USB cable for camera if USB.
- (Optional) Short USB cable for IR pen if powered from Pi.

Last updated: 2025-03-04
