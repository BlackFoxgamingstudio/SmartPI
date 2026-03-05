# Build Guide

Step-by-step setup from a fresh Pi to “demo running” with interactive projection.

## Prerequisites

- Raspberry Pi 4 or 5 with Raspberry Pi OS (or compatible Linux).
- HDMI projector and camera (see [01_bill_of_materials.md](01_bill_of_materials.md)).
- Network (for `pip install`; or pre-download dependencies).

## 1. Prepare the Pi

1. Flash Raspberry Pi OS to a microSD card; enable SSH if needed.
2. Boot the Pi, update: `sudo apt update && sudo apt upgrade`.
3. (Optional) Increase GPU memory for display: `sudo raspi-config` → Performance Options → GPU Memory (e.g. 256).

## 2. Install system dependencies

```bash
sudo apt install -y python3-pip python3-venv libopencv-dev python3-opencv \
  libsdl2-dev libsdl2-image-dev libportmidi-dev
```

For CSI camera with libcamera:

```bash
sudo apt install -y libcamera-dev python3-libcamera
```

To use the libcamera capture path on Pi, set `use_libcamera: true` in `configs/app.yaml` and install the `picamera2` package (e.g. `pip install picamera2`); it is not in requirements.txt.

## 3. Clone and install the project

```bash
git clone https://github.com/YOUR_ORG/rashbarrypi.git
cd rashbarrypi
./scripts/install_pi.sh
# Or manually: pip install -r requirements.txt
# For development (editable install): pip install -e .
```

## 4. Connect hardware

- Connect projector via HDMI. Set resolution (e.g. 1920×1080) in **Raspberry Pi Configuration** → **Display** → **Resolution** (or via `raspi-config` → Display Options).
- Connect camera (USB or CSI). **Ensure it is detected:** for USB, `ls /dev/video*` should list at least `/dev/video0`; for CSI, run `libcamera-hello --list-cameras` and confirm your camera appears. If nothing appears, enable the camera in `raspi-config` (Interface Options → Camera) and reboot.
- **Screen blanking** is when the display turns off after a period of inactivity. Disable it so the projection stays on: Raspberry Pi Configuration → Display → Screen Blanking → Disable.

## 5. Run healthcheck

```bash
./scripts/healthcheck.sh
# Or directly: smartpi healthcheck
```

Fix any reported issues (no camera, no display, low FPS) before continuing. See [07_troubleshooting.md](07_troubleshooting.md).

## 6. Calibrate (first time)

Run the calibration wizard so camera coordinates map to projector coordinates:

```bash
smartpi calibrate
```

**4-corner flow:** Tap each of the four corner targets in order when the app prompts you; calibration is saved to `configs/calibration.yaml`. See [05_calibration_ux.md](05_calibration_ux.md).

## 7. Run the demo

```bash
smartpi run
# Or fullscreen / kiosk:
smartpi run --fullscreen
```

Choose a scene (e.g. Sandbox Draw, Particle Field) and use the pointer to interact.

## 8. (Optional) Kiosk mode

**Kiosk mode** means the app starts automatically at boot (e.g. after login or from a minimal session) and runs fullscreen so the Pi acts as a dedicated interactive display without other UI.

- Copy `src/smartpi/services/systemd/smartpi.service` to `/etc/systemd/system/`, edit paths, then `sudo systemctl enable smartpi`.
- Or use the autostart desktop file in `src/smartpi/services/autostart/` for a graphical autostart.

## 9. (Optional) Develop on x86 without Pi hardware

A development Docker image lets you run the app and tests on x86 (e.g. your laptop) without Raspberry Pi hardware. Camera and display will be limited or mocked.

```bash
docker build -f docker/Dockerfile.dev -t smartpi-dev .
docker run --rm -it smartpi-dev make test
# Or shell in: docker run --rm -it smartpi-dev bash
```

See [04_system_architecture.md](04_system_architecture.md) for pipeline details and [07_troubleshooting.md](07_troubleshooting.md) for common problems.

Last updated: 2026-03-04
