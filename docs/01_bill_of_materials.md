# Bill of Materials (BOM)

**Canonical** here means the authoritative part list for building the Smart Pi setup; replicate from this list for a supported build. The BOM supports the **Starter Kit** (Smart Kit) target of **~$215 per kit** — equip 10 classrooms for ~$2,150 instead of $20,000 with traditional EdTech. For a machine-readable list, see [hardware/bom.csv](../hardware/bom.csv). Print from CLI: `smartpi bom` (and `smartpi bom --pen` for the IR pen BOM). API: `smartpi.core.bom` — see [api_overview.md](api_overview.md).

## Hardware stack (PDF-aligned)

| Role | Component | Notes |
|------|-----------|--------|
| **Brain** | Raspberry Pi 5 (4GB) or Pi 4 | Bookworm OS recommended |
| **Bridge** | Active micro-HDMI to VGA (or HDMI) adapter, 3.5mm audio | Pi to projector; surplus projectors often VGA |
| **Tracker** | Pi Camera v3 or Bluetooth Wii Remote | IR tracking for pen dot |
| **Muscle** | Surplus/thrifted projector | e.g. Epson XGA 1024×768; see [compatibility](#compatibility-matrix) |
| **Input** | Student-built IR pen | IR LED, momentary switch, AAA holder — see [hardware/ir_pen](../hardware/ir_pen/) |

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

- HDMI cable (Pi → projector). **Video adapters:** micro-HDMI to HDMI (Pi 4/5); micro-HDMI to VGA (active) + 3.5mm audio if the surplus projector has only VGA.
- USB cable for camera if USB.
- (Optional) Short USB cable for IR pen if powered from Pi.

## Mounting and rigging

- Tripod, table clamp, or brackets for camera and projector so the demo is stable. See [hardware/camera_mount](../hardware/camera_mount/), [hardware/enclosure](../hardware/enclosure/). For event/showcase needs see [10_event_and_venue_requirements.md](10_event_and_venue_requirements.md).

## Power and safety

- **Raspberry Pi:** Fused 5V/5A USB-C (isolated from projector). See [08_safety_and_power.md](08_safety_and_power.md).
- Power strip (and extension cord if needed), gaff tape or cable management, labels for cables.

## Contingency spares

- Backup HDMI cable and backup adapter(s) to avoid single-point failure during a hackathon or showcase.

## Projection surface (optional)

- Portable screen material or whiteboard film when the venue wall is not suitable for consistent calibration.

## Compatibility matrix

- Maintain a **compatibility matrix** of known-good projector models (e.g. Epson EMP-83H) with lamp IDs where relevant. Centralizing a small buffer (30–50 units) helps mitigate inconsistent projector supply. See [03_repair_forward_notes.md](03_repair_forward_notes.md) for surplus sourcing.

Last updated: 2026-03-04
