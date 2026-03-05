# Troubleshooting

Common problems and what to try.

## No camera detected

- **Check connection:** Re-seat USB or CSI cable; try another port.
- **Linux:** `ls /dev/video*` (USB) or `libcamera-hello --list-cameras` (CSI). If nothing appears, enable camera in `raspi-config` (Interface Options → Camera) for CSI.
- **Permissions:** Ensure the user is in the `video` group: `groups` and if needed `sudo usermod -aG video $USER` (then log out and back in).
- **Config:** In `configs/app.yaml`, set the correct `camera_index` (often 0 for first device).

## Low FPS

- **Resolution:** Lower capture resolution in `configs/app.yaml` to reduce load.
- **Exposure:** Lock exposure if the camera supports it to avoid per-frame auto-adjustment.
- **Thermal:** Check Pi temperature; ensure cooling. Throttling will reduce FPS.
- **Other apps:** Close browsers and heavy apps; run headless or with a light desktop if possible.
- **Profile:** Try `configs/profiles/dark_room.yaml` or `daylight.yaml` to match lighting and reduce unnecessary work.

## Bad alignment (cursor not where pointer is)

- **Recalibrate:** Run `smartpi calibrate` again. Ensure all 4 corners are tapped accurately and the pointer is steady.
- **Camera movement:** If the camera was moved, calibration is invalid; recalibrate.
- **Validation:** After calibration, check the reported reprojection error; if high, repeat calibration or adjust camera angle/position.
- **Lens distortion:** The current pipeline uses a homography (planar); strong lens distortion may need a future distortion model.

## Lighting

- **Too bright:** Detection may fail or jitter. Use a darker profile, reduce ambient light, or increase pointer brightness (e.g. IR pen intensity).
- **Too dark:** Increase exposure or use a profile tuned for dark rooms; ensure the pointer is still visible to the camera.
- **Profiles:** Switch `configs/profiles/` (classroom, daylight, dark_room) to match the environment.

## App won’t start or crashes

- **Dependencies:** Run `pip install -r requirements.txt` (or `make install`). Ensure Python 3.10+.
- **Display:** If running headless, ensure a virtual display or run with a connected projector/monitor. Pygame needs a display.
- **Logs:** Check terminal output or logs; run `smartpi healthcheck` or `./scripts/healthcheck.sh`.

For hardware compatibility reports, use the [hardware compat issue template](../.github/ISSUE_TEMPLATE/hardware_compat.yml).

Last updated: 2025-03-04
