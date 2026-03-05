# Showcase Script

Short script for presenting the Smart Pi demo (e.g. at a hackathon or workshop).

## Before the demo

1. Confirm the venue meets [event and venue requirements](../10_event_and_venue_requirements.md) (space, power, lighting, throw, spares).
2. Power on the Pi and projector; wait for the system to boot.
3. If the app does not autostart, run `smartpi run` (or `./scripts/run_demo.sh`).
4. If this is a new setup or the camera moved, run calibration: **Calibrate** from the menu or `smartpi calibrate`; complete the 4 corners in under 2 minutes.
5. Verify the pointer is detected (you should see a cursor or overlay following the pen/pointer).

## During the demo (about 30 seconds)

1. **Start** — From the main menu, choose “Start” or “Demo.”
2. **Sandbox Draw** — Select the drawing scene. Show that the pointer draws where the pen touches; try the corner color hotzones to change color.
3. **Particle Field** — Switch to the particle scene. Show that the pointer “pushes” particles and interacts in real time.
4. **Repo** — Optionally open the repo and show: BOM, build guide, “how calibration works,” and how to add a new scene (see CONTRIBUTING and `src/smartpi/renderer/scenes/`).

## After

- Exit the app cleanly (menu or Ctrl+C if running in terminal).
- For a long-running installation, consider shutdown via the Pi menu or `sudo shutdown -h now`.

See [operator_checklist.md](operator_checklist.md) for a quick checklist.

Last updated: 2026-03-04
