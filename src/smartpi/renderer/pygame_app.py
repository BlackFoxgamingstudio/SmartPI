"""Default demo app for Smart Pi Projector: Kiosk web UI with plugin scene loaders.

Motion to input: capture (camera/Wii Remote, IR pen) → detect → track →
4-point auto-calibration (homography) → interact (OS-level mouse events).
Scenes: Sandbox Draw, Particle Field, STEM Widgets (plugin scene loaders).
"""

from __future__ import annotations

from pathlib import Path

import pygame

from smartpi.core.capture import CameraCapture, create_capture
from smartpi.core.timing import FPSCounter
from smartpi.vision.detect_bright import detect_bright_point
from smartpi.vision.detect_ir import detect_ir_blob
from smartpi.vision.track import SmoothingTracker
from smartpi.vision.calibrate import load_calibration, apply_homography
from smartpi.ui.overlay import draw_overlay
from smartpi.interaction.gesture import emit_events_from_track
from smartpi.interaction.events import PointerState
from smartpi.interaction.adapters.pygame_adapter import pygame_event_from_pointer
from smartpi.renderer.scenes.sandbox_draw import SandboxDrawScene
from smartpi.renderer.scenes.particle_field import ParticleFieldScene
from smartpi.renderer.scenes.stem_widgets import StemWidgetsScene


def _load_config(config_dir: str) -> dict:
    import yaml
    path = Path(config_dir) / "app.yaml"
    if not path.exists():
        return {"camera_index": 0, "resolution": [640, 480], "detector": "bright", "threshold": 200}
    with open(path) as f:
        app = yaml.safe_load(f) or {}
    profile_name = app.get("profile", "classroom")
    profile_path = Path(config_dir) / "profiles" / f"{profile_name}.yaml"
    if profile_path.exists():
        with open(profile_path) as pf:
            profile = yaml.safe_load(pf) or {}
        profile.pop("profile", None)
        app = {**app, **profile}
    return app


def run_app(fullscreen: bool = False, config_dir: str = "configs") -> None:
    """Run the interactive projection app with scene selector and demo scenes."""
    from smartpi.core.logging_config import configure_logging
    configure_logging(config_dir)
    config = _load_config(config_dir)
    cam_index = config.get("camera_index", 0)
    res = config.get("resolution", [640, 480])
    w, h = res[0], res[1]
    detector = config.get("detector", "bright")
    threshold = config.get("threshold", 200)
    blur = config.get("blur", 3)

    calibration = load_calibration(Path(config_dir) / "calibration.yaml")
    proj_w = proj_h = 640
    if calibration and "resolution" in calibration:
        proj_w = calibration["resolution"][0]
        proj_h = calibration["resolution"][1]
    else:
        profile_name = config.get("projector_profile")
        if profile_name:
            from smartpi.core.projector_profile import load_projector_profile
            repo_root = Path(config_dir).resolve().parent
            profile = load_projector_profile(repo_root, profile_name)
            if profile and "resolution" in profile:
                res_p = profile["resolution"]
                if len(res_p) >= 2:
                    proj_w, proj_h = int(res_p[0]), int(res_p[1])

    pygame.init()
    if fullscreen:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((proj_w, proj_h), pygame.RESIZABLE)
    pygame.display.set_caption("Smart Pi Projector")
    width, height = screen.get_size()

    use_libcamera = config.get("use_libcamera", False)
    capture = create_capture(cam_index, w, h, 30.0, use_libcamera)
    if not capture.open():
        pygame.quit()
        raise RuntimeError("Could not open camera")
    fps_counter = FPSCounter(30)
    use_kalman = config.get("use_kalman", False)
    tracker = SmoothingTracker(alpha=0.3, use_kalman=use_kalman)

    scenes = {
        "1": SandboxDrawScene(width, height),
        "2": ParticleFieldScene(width, height),
        "3": StemWidgetsScene(width, height),
    }
    current_scene: str | None = None
    scene_obj = None
    show_overlay = True
    prev_xy: tuple[float, float] | None = None
    prev_down = False

    clock = pygame.time.Clock()
    running = True
    pointer: tuple[float, float] | None = None

    def camera_to_proj(cx: float, cy: float) -> tuple[float, float]:
        if calibration and "homography" in calibration:
            return apply_homography(calibration["homography"], cx, cy)
        return (cx, cy)

    try:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if current_scene:
                            current_scene = None
                            scene_obj = None
                        else:
                            running = False
                    if event.key == pygame.K_1:
                        current_scene = "1"
                        scene_obj = SandboxDrawScene(width, height)
                    if event.key == pygame.K_2:
                        current_scene = "2"
                        scene_obj = ParticleFieldScene(width, height)
                    if event.key == pygame.K_3:
                        current_scene = "3"
                        scene_obj = StemWidgetsScene(width, height)
                    if event.key == pygame.K_o:
                        show_overlay = not show_overlay

            ret, frame = capture.read()
            if not ret or frame is None:
                screen.fill((20, 20, 20))
                if scene_obj:
                    scene_obj.draw(screen)
                if show_overlay:
                    draw_overlay(screen, fps_counter.fps(), None, threshold)
                pygame.display.flip()
                clock.tick(10)
                continue

            if detector == "ir":
                pt = detect_ir_blob(frame, threshold=threshold, blur_ksize=blur)
            else:
                pt = detect_bright_point(frame, threshold=threshold, blur_ksize=blur)

            if pt is not None:
                proj_pt = camera_to_proj(pt[0], pt[1])
                pointer = tracker.update(proj_pt[0], proj_pt[1])
            else:
                tracker.reset()
                pointer = None

            # Emit pointer events for scene
            for ev in emit_events_from_track(pointer, prev_xy, prev_down):
                if scene_obj and hasattr(scene_obj, "on_pointer"):
                    scene_obj.on_pointer(pygame_event_from_pointer(ev))
            if pointer is not None:
                prev_xy = pointer
                prev_down = True
            else:
                prev_xy = None
                prev_down = False

            if scene_obj:
                if hasattr(scene_obj, "update"):
                    scene_obj.update()
                scene_obj.draw(screen)
            else:
                screen.fill((20, 20, 20))
                font = pygame.font.Font(None, 48)
                msg = "1=Draw 2=Particles 3=STEM O=Overlay Esc=Back/Quit"
                text = font.render(msg, True, (200, 200, 200))
                screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - 24))
            if show_overlay:
                draw_overlay(screen, fps_counter.fps(), pointer, threshold)
            fps_counter.tick()
            pygame.display.flip()
            clock.tick(30)
    finally:
        capture.release()
        pygame.quit()
