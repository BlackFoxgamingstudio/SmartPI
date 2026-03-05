# Repair-Forward Notes

Notes on sourcing and maintaining hardware so the setup can be repaired and replicated. Smart Pi is inspired by the **Framework laptop ethos**: not a sealed black box — **the kit is the curriculum**. Students assemble hardware, learn optics, flash the OS, and perform standard maintenance (repair literacy, technical confidence). *A transition from planned obsolescence to planned repair.*

## Circular supply chain

- **Divert** — Partner with e-waste recyclers to rescue functional XGA projectors. Local sourcing via SOP (schools or gig-worker/Task-Rabbit style) from reuse shops or district surplus.
- **Upcycle** — Extend the useful life of existing hardware with Pi-powered brains (Smart Kit: Pi, camera, cables, adapters, IR parts; drop-shipped ~$200).
- **Maintain** — Empower local repair capacity; projectors become mobile, transferable assets. Right-to-Repair aligned; attractive for sustainability/ESG and STEM micro-grants.

## Surplus projectors

- Many used projectors work well for this project (720p/1080p HDMI).
- Check: HDMI input, native resolution, lamp life (or LED). Replace lamp if dim or failing.
- Keep vents clear; avoid blocking airflow to reduce overheating.
- If the projector has a “whiteboard” or “interactive” mode, we do not rely on it; we use our own camera-based tracking.

## Common fixes

- **No image:** Check HDMI cable and input selection; try another port or cable. Ensure Pi output resolution is supported.
- **Camera not detected:** Re-seat USB/CSI; check `dmesg` for errors; try another port. On Pi, enable camera in `raspi-config` if using CSI.
- **Low FPS:** Reduce resolution in config; lock exposure if supported; close other apps. See [07_troubleshooting.md](07_troubleshooting.md).
- **Pointer not detected:** Adjust detection thresholds in `configs/app.yaml` or use a profile from `configs/profiles/` (classroom, dark_room, daylight). Ensure pointer is bright/visible to the camera.

## Sourcing parts

- **Pi:** Official resellers or Raspberry Pi Foundation.
- **Projector:** Local surplus, eBay, or office clearouts.
- **Camera:** Standard USB webcam or Pi Camera Module; for IR, choose a model without a strong IR cut filter or add an IR-pass filter.
- **IR pen:** See [hardware/ir_pen/](../hardware/ir_pen/) for BOM and wiring.

## Replication

To replicate this setup elsewhere, use the [Bill of materials](01_bill_of_materials.md), this build guide ([02_build_guide.md](02_build_guide.md)), and the same config layout. Calibration is per-installation and stored in `configs/calibration.yaml` (not committed).

## Compatibility matrix and scaling

- **Compatibility matrix:** Maintain a list of 5+ known-good projector models (e.g. Epson EMP-83H) with lamp IDs; centralize a small buffer (30–50 units) to mitigate inconsistent supply. See [01_bill_of_materials.md](01_bill_of_materials.md)#compatibility-matrix.
- **Scaling (first 6 months):** MVP & pilots (25–50 R&D pilot kits; v1 documentation, safety SOPs, compatibility matrix); local scaling (MOUs with e-waste recyclers, gig-worker sourcing SOP, $99/school update plan); district rollouts (30–100 kit deals, teacher PD webinars, STEM/Sustainability micro-grants).
- **Support:** $99/year paid tier reserves direct email/phone for schools; DIY users are steered to community forums and documentation.

Last updated: 2026-03-04
