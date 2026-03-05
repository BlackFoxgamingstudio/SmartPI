# Calibration UX

Calibration maps camera coordinates to projector coordinates so the projected cursor aligns with the physical pointer.

## Flow (4-corner)

The **4-corner flow** means: the app shows four targets in a fixed order (typically top-left, top-right, bottom-right, bottom-left); you tap each target once with the pointer when prompted; the app records the pointer position in camera space for that corner and then moves to the next. After all four, it solves the homography and saves the result.

1. App projects **4 corner targets** (large, high-contrast, at least 80×80 px) on the surface in order: top-left → top-right → bottom-right → bottom-left.
2. User **taps each target** with the IR pen or holds the pointer steady on it.
3. App records pointer position in **camera space** for each corner.
4. **Homography** is solved from the 4 point correspondences; result is saved to `configs/calibration.yaml`.
5. **Validation:** App can project a crosshair grid; user taps 1–2 points; we compute reprojection error and warn if poor.

Target: calibration completable in **under 2 minutes** by a new user (from “start calibration” to “calibration saved,” excluding boot time). Big “Next” buttons (min 44×44 pt), minimal typing.

## Validation

- **Reprojection error** measures how well the homography fits: for known projector-space points we transform to camera space (or the reverse) and compare to the detected positions; we report the **median** distance in **projector pixels** over the validation points.
- After calibration, median error at 1080p should be within a tolerable band: **&lt; 15 px** for a demo-quality setup. The exact threshold is in the vision/calibration code.
- If error is high, suggest re-running calibration or adjusting camera position/angle.
- See [07_troubleshooting.md](07_troubleshooting.md) for “bad alignment.”

## Screenshots and diagrams

Add screenshots under [docs/images/](images/) with descriptive alt text for accessibility:

- **Calibration wizard:** `calibration_wizard.png` — Four corner targets on the projection surface during calibration step 1.
- **Validation grid:** `validation_grid.png` — Crosshair grid shown after calibration for validation tap.

Example in markdown: `![Four corner targets on the projection surface during calibration](images/calibration_wizard.png)`.

Diagram: [diagrams/calibration_flow.mmd](diagrams/calibration_flow.mmd).

Last updated: 2025-03-04
