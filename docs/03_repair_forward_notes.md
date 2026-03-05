# Repair-Forward Notes

Notes on sourcing and maintaining hardware so the setup can be repaired and replicated.

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

Last updated: 2025-03-04
