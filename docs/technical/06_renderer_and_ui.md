# Renderer and UI: Logic and Data In/Out

This document describes the renderer (main Pygame app loop, scene selector, and demo scenes) and the UI components (calibration wizard and overlay). For each component we specify inputs, outputs, and the logic that ties capture, detection, tracking, homography, and events to the final display and user feedback.

## Role of the renderer and UI

The renderer consumes the full pipeline: it owns the capture, runs the detector and tracker, applies homography, emits pointer events, and draws the active scene plus an optional overlay. It is the only place where “one frame” is executed end-to-end. The calibration wizard is a separate flow: it uses capture and detection to collect four camera-space points, solves and saves homography, and optionally runs a validation step. The overlay is a small drawing layer (FPS, threshold, pointer position, and a green circle at the pointer) that is drawn on top of the scene. All coordinates in the renderer and overlay are in **projector/display space** (pixels).

---

## Main app: `run_app(fullscreen, config_dir)`

**Module:** `smartpi.renderer.pygame_app`

**Purpose:** Run the interactive projection app: open camera and display, load config and calibration, create tracker and scenes, then run the main loop. No return until the user quits.

**Inputs:**
- `fullscreen` (bool): if True, use Pygame fullscreen (FULLSCREEN flag); else windowed resizable.
- `config_dir` (str): path to config directory (e.g. `"configs"`).

**Outputs:** None. Raises on failure (e.g. camera open failed).

**Logic (high level):**
1. **Config:** Call internal `_load_config(config_dir)` (reads app.yaml, no profile merge in this helper; the code uses a simple path and defaults). Get camera_index, resolution [w,h], detector, threshold, blur.
2. **Calibration:** `load_calibration(Path(config_dir) / "calibration.yaml")`. If present, read resolution from calibration for display size; else use projector_profile from config (from hardware/projector_profiles/) or default (e.g. 640×640).
3. **Pygame init:** Set display mode (fullscreen or (proj_w, proj_h) resizable), caption "Smart Pi". Get actual width, height from screen.
4. **Capture:** `create_capture(cam_index, w, h, fps, config.get("use_libcamera", False))` and `capture.open()`; on failure raise RuntimeError and quit Pygame.
5. **Timing and tracking:** `FPSCounter(30)`, `SmoothingTracker(alpha=0.3, use_kalman=config.get("use_kalman", False))`.
6. **Scenes:** Build dict "1" → SandboxDrawScene, "2" → ParticleFieldScene, "3" → StemWidgetsScene (each gets width, height). current_scene and scene_obj start None; show_overlay True; prev_xy None, prev_down False.
7. **Helper:** `camera_to_proj(cx, cy)`: if calibration and homography exist, return `apply_homography(calibration["homography"], cx, cy)`; else return (cx, cy).
8. **Main loop (while running):**
   - **Pygame events:** QUIT → running = False. KEYDOWN: Escape → back out of scene or quit; 1/2/3 → set current_scene and new scene instance; O → toggle show_overlay.
   - **Read frame:** `ret, frame = capture.read()`. If not ret or frame None: fill screen, draw scene if any, draw overlay if show_overlay, flip, clock.tick(10); continue.
   - **Detect:** If detector "ir" then `pt = detect_ir_blob(frame, ...)` else `pt = detect_bright_point(frame, ...)`. pt is (cx, cy) or None.
   - **Project and track:** If pt not None: (px, py) = camera_to_proj(pt[0], pt[1]); pointer = tracker.update(px, py). Else: tracker.reset(); pointer = None.
   - **Events:** For each ev in emit_events_from_track(pointer, prev_xy, prev_down): if scene has on_pointer, scene.on_pointer(pygame_event_from_pointer(ev)). Then set prev_xy = pointer, prev_down = (pointer is not None).
   - **Draw:** If scene_obj: call update() if present, then scene_obj.draw(screen). Else: fill and show "1=Draw 2=Particles ...".
   - **Overlay:** If show_overlay, draw_overlay(screen, fps_counter.fps(), pointer, threshold).
   - **Tick:** fps_counter.tick(), pygame.display.flip(), clock.tick(30).
9. **Exit:** finally: capture.release(), pygame.quit().

**Data flow in one iteration:** frame (BGR) → detect → (cx,cy) or None → camera_to_proj → tracker.update → pointer (or None) → emit_events_from_track → on_pointer(dict) per event → prev_xy/prev_down update → scene.update/draw → overlay → flip. So the renderer is the orchestrator; it does not return data to the rest of the system except via the display surface and (conceptually) any adapter (WebSocket/uinput) if wired in.

---

## Scenes: SandboxDrawScene, ParticleFieldScene, StemWidgetsScene

All scenes are constructed with `(width, height)` (display size). They implement at least `draw(surface)` and optionally `on_pointer(ev)` and `update()`. **StemWidgetsScene** implements ruler (tap two points → segment + length label), angles (tap vertex + two rays → angle in degrees), and graph paper (grid + snap). Mode is cycled via the top-left hotzone; top-right hotzone clears. It is no longer a stub.

**SandboxDrawScene:**  
- **on_pointer(ev):** ev is dict with "x", "y", "state". Top-left corner hotzone (margin = min(w,h)//8): if (x,y) in corner, cycle color and return. Else: state "down" → start new stroke (current_stroke = [(x,y)]); "move" and stroke non-empty → append (x,y); "up" and stroke non-empty → append (x,y), push stroke to lines, clear current_stroke.  
- **draw(surface):** Fill dark blue; draw all lines and current_stroke as lines with current color; draw "Top-left: change color" hint at bottom.  
- **Data in:** on_pointer receives dict; draw receives Pygame Surface. No return values.

**ParticleFieldScene:**  
- **on_pointer(ev):** Store pointer_xy = (ev["x"], ev["y"]). If state in ("down", "move"), call particle.push(ev["x"], ev["y"]) for each particle. If state "up", set pointer_xy = None.  
- **update():** For each particle, particle.update(width, height) (physics: move, damp, bounce off edges).  
- **draw(surface):** Fill dark; draw particles as circles; if pointer_xy set, draw yellow circle at pointer.  
- **Particle.push(px, py, strength):** Repulsion from (px, py); add velocity away from pointer, inverse-square falloff.  
- **Data in/out:** Same pattern: events in, draw surface in; no return values.

**StemWidgetsScene:** Same interface (on_pointer, update if present, draw). Ruler: two taps define a segment with length label. Angles: vertex tap then two ray taps show angle in degrees. Graph paper: grid with snap. Top-left hotzone cycles mode; top-right clears. Data contract is identical: dict for on_pointer, Surface for draw.

---

## Overlay: `draw_overlay(surface, fps, pointer_xy, threshold)`

**Module:** `smartpi.ui.overlay`

**Purpose:** Draw debug text (FPS, threshold, pointer position) and a green circle at the pointer on the given surface.

**Inputs:**
- `surface`: Pygame Surface (the screen).
- `fps`: float (current FPS).
- `pointer_xy`: (x, y) in display coords or None.
- `threshold`: int; if 0, threshold line is not drawn.

**Outputs:** None. Draws on surface in-place.

**Logic:** Font None (default), size 36. Lines: "FPS: {fps:.1f}"; if threshold>0 add "Thr: {threshold}"; if pointer_xy add "Ptr: {x}, {y}". Blit each line at (10, y) with y incrementing. If pointer_xy set, draw a circle at (int(px), int(py)), color green, radius 8, width 2.

---

## Calibration wizard: `run_wizard(config_dir, use_pygame=True)` and `_run_wizard_pygame` / `_run_wizard_opencv`

**Module:** `smartpi.ui.calibration_wizard`

**run_wizard:** If use_pygame True, try `_run_wizard_pygame(config_dir)`; on exception fall back to `_run_wizard_opencv(config_dir)`. So the Pygame wizard is primary (fullscreen, big targets, validation); OpenCV is fallback (window, mouse click 4 corners).

**Pygame wizard (summary):** Load config (resolution, camera_index, detector, threshold, blur). Open CameraCapture, init Pygame fullscreen at PROJ_W×PROJ_H (1920×1080). State machine: "target" (show one of 4 corner targets, wait for user to hold pointer on it, detect and record camera point, then Next); "solving" (solve_homography, save_calibration); "validate_1"/"validate_2" (e.g. tap center, tap top-left, compute reprojection_error, show median error); "done". Detection each frame: same as main app (detect_ir or detect_bright). When target is visible, the wizard waits for a stable detection on the target, then records that (cx, cy) and moves to next corner or to solving. Pointer feedback: green dot at scaled camera position so user sees where the system thinks the pointer is. All four camera points + fixed DST_PTS (four projector corners) are passed to solve_homography; the result is saved to config_dir/calibration.yaml.

**Data in (wizard):** config_dir; config file; camera stream. **Data out:** Written calibration.yaml; no return value. Validation step uses reprojection_error and displays the result; it does not modify the saved file.

**OpenCV wizard:** Simpler: one window, user clicks four corners with the mouse; callback records (x,y) in image coords; after 4 points, solve_homography and save_calibration; no validation step. Same DST_PTS. Input: config_dir and camera. Output: calibration.yaml.

---

## Summary: data in and out

| Component        | Data in                               | Data out / side effect           |
|------------------|----------------------------------------|----------------------------------|
| run_app          | fullscreen, config_dir                 | None; drives display and scenes  |
| _load_config     | config_dir                             | dict (camera, res, detector, …)  |
| Scene on_pointer| event dict                             | None (state change)              |
| Scene draw       | Pygame Surface                         | None (pixels on surface)         |
| Scene update     | (none)                                 | None                             |
| draw_overlay     | surface, fps, pointer_xy, threshold    | None (draw on surface)           |
| run_wizard       | config_dir, use_pygame                 | None; writes calibration.yaml    |

The next document covers the CLI, config loading, healthcheck, and diagnostics in full detail.

Last updated: 2026-03-04
