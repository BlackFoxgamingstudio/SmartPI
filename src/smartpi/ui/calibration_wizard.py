"""Calibration wizard: 4-corner flow with big buttons, optional validation step."""

from __future__ import annotations

from pathlib import Path

import pygame
import yaml

from smartpi.vision.calibrate import (
    solve_homography,
    save_calibration,
    apply_homography,
)
from smartpi.core.capture import CameraCapture
from smartpi.vision.detect_bright import detect_bright_point
from smartpi.vision.detect_ir import detect_ir_blob

# Corner positions in projector space (normalized 0-1 for drawing)
CORNER_POSITIONS = [(0.15, 0.15), (0.85, 0.15), (0.85, 0.85), (0.15, 0.85)]
CORNER_NAMES = ["Top-left", "Top-right", "Bottom-right", "Bottom-left"]
PROJ_W, PROJ_H = 1920, 1080
DST_PTS = [(0, 0), (PROJ_W, 0), (PROJ_W, PROJ_H), (0, PROJ_H)]


def _run_wizard_opencv(config_dir: str) -> None:
    """Fallback: OpenCV window, click 4 corners with mouse. For headless or no Pygame display."""
    import cv2
    import numpy as np
    from smartpi.vision.calibrate import solve_homography, save_calibration

    config_path = Path(config_dir) / "app.yaml"
    res = [640, 480]
    cam_index = 0
    if config_path.exists():
        with open(config_path) as f:
            app = yaml.safe_load(f) or {}
            res = app.get("resolution", res)
            cam_index = app.get("camera_index", 0)
    w, h = res[0], res[1]
    src_pts: list[tuple[float, float]] = []
    capture = CameraCapture(cam_index, w, h)
    if not capture.open():
        raise RuntimeError("Could not open camera")
    window = "Calibration: click 4 corners (top-left, top-right, bottom-right, bottom-left)"
    cv2.namedWindow(window)

    def on_mouse(event: int, x: int, y: int, *_: object) -> None:
        if event == cv2.EVENT_LBUTTONDOWN and len(src_pts) < 4:
            src_pts.append((float(x), float(y)))
            print(f"Point {len(src_pts)}: ({x}, {y})")

    cv2.setMouseCallback(window, on_mouse)
    print("Click the 4 corners in order: top-left, top-right, bottom-right, bottom-left.")
    while len(src_pts) < 4:
        ret, frame = capture.read()
        if not ret:
            continue
        for i, (px, py) in enumerate(src_pts):
            cv2.circle(frame, (int(px), int(py)), 10, (0, 255, 0), 2)
            cv2.putText(frame, str(i + 1), (int(px) + 12, int(py)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow(window, frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    capture.release()
    cv2.destroyAllWindows()
    if len(src_pts) != 4:
        print("Need exactly 4 points. Aborted.")
        return
    H = solve_homography(src_pts, DST_PTS)
    if H is None:
        print("Failed to solve homography.")
        return
    out_path = Path(config_dir) / "calibration.yaml"
    save_calibration(out_path, H, (0, 0, PROJ_W, PROJ_H), (PROJ_W, PROJ_H))
    print(f"Calibration saved to {out_path}")


def run_wizard(config_dir: str = "configs", use_pygame: bool = True) -> None:
    """Run 4-corner calibration. Uses Pygame with big buttons by default; falls back to OpenCV if no display."""
    if use_pygame:
        try:
            _run_wizard_pygame(config_dir)
            return
        except Exception as e:
            print(f"Pygame wizard failed ({e}), falling back to OpenCV.")
    _run_wizard_opencv(config_dir)


def _run_wizard_pygame(config_dir: str) -> None:
    """Pygame wizard: fullscreen, big targets, big Next button, then validation step."""
    config_path = Path(config_dir) / "app.yaml"
    res = [640, 480]
    cam_index = 0
    detector = "bright"
    threshold = 200
    blur = 3
    if config_path.exists():
        with open(config_path) as f:
            app = yaml.safe_load(f) or {}
        profile_name = app.get("profile", "classroom")
        profile_path = Path(config_dir) / "profiles" / f"{profile_name}.yaml"
        if profile_path.exists():
            with open(profile_path) as pf:
                profile = yaml.safe_load(pf) or {}
            profile.pop("profile", None)
            app = {**app, **profile}
        res = app.get("resolution", res)
        cam_index = app.get("camera_index", 0)
        detector = app.get("detector", "bright")
        threshold = app.get("threshold", 200)
        blur = app.get("blur", 3)
    w, h = res[0], res[1]

    capture = CameraCapture(cam_index, w, h)
    if not capture.open():
        raise RuntimeError("Could not open camera")

    pygame.init()
    screen = pygame.display.set_mode((PROJ_W, PROJ_H), pygame.FULLSCREEN | pygame.DOUBLEBUF)
    pygame.display.set_caption("Smart Pi Calibration")
    font_large = pygame.font.Font(None, 72)
    font_btn = pygame.font.Font(None, 56)
    clock = pygame.time.Clock()
    src_pts: list[tuple[float, float]] = []
    state = "target"  # target, solving, validate_1, validate_2, done
    target_index = 0
    val_pts: list[tuple[float, float]] = []
    val_expected = [(PROJ_W / 2, PROJ_H / 2), (PROJ_W / 4, PROJ_H / 4)]
    H_solved = None  # set after solving; used in done for error
    error_px: float | None = None
    last_pointer: tuple[float, float] | None = None

    try:
        while True:
            # Capture and detect pointer
            ret, frame = capture.read()
            if ret and frame is not None:
                if detector == "ir":
                    pt = detect_ir_blob(frame, threshold=threshold, blur_ksize=blur)
                else:
                    pt = detect_bright_point(frame, threshold=threshold, blur_ksize=blur)
                last_pointer = pt
            else:
                last_pointer = None

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    state = "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        state = "quit"
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        if state == "target" and target_index < 4 and last_pointer is not None:
                            src_pts.append(last_pointer)
                            target_index += 1
                            if target_index >= 4:
                                state = "solving"
                        elif state == "validate_1" and last_pointer is not None:
                            val_pts.append(last_pointer)
                            state = "validate_2"
                        elif state == "validate_2" and last_pointer is not None:
                            val_pts.append(last_pointer)
                            state = "done"
                        elif state == "done":
                            state = "quit"
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    # Big Next button: bottom center, ~400x80
                    btn = pygame.Rect(PROJ_W // 2 - 200, PROJ_H - 120, 400, 80)
                    if btn.collidepoint(mx, my):
                        if state == "target" and target_index < 4 and last_pointer is not None:
                            src_pts.append(last_pointer)
                            target_index += 1
                            if target_index >= 4:
                                state = "solving"
                        elif state == "validate_1" and last_pointer is not None:
                            val_pts.append(last_pointer)
                            state = "validate_2"
                        elif state == "validate_2" and last_pointer is not None:
                            val_pts.append(last_pointer)
                            state = "done"
                        elif state == "done":
                            state = "quit"

            screen.fill((30, 30, 40))

            if state == "target" and target_index < 4:
                # Draw target circle in corner
                cx = int(CORNER_POSITIONS[target_index][0] * PROJ_W)
                cy = int(CORNER_POSITIONS[target_index][1] * PROJ_H)
                pygame.draw.circle(screen, (255, 200, 0), (cx, cy), 60, 6)
                text = font_large.render(
                    f"Tap {CORNER_NAMES[target_index]} then press Next",
                    True,
                    (255, 255, 255),
                )
                screen.blit(text, (PROJ_W // 2 - text.get_width() // 2, 80))
                if last_pointer is not None:
                    # Scale camera coords to projector (display) coords for feedback
                    px = int(last_pointer[0] * PROJ_W / w)
                    py = int(last_pointer[1] * PROJ_H / h)
                    pygame.draw.circle(screen, (0, 255, 0), (px, py), 15, 3)
                # Next button
                btn = pygame.Rect(PROJ_W // 2 - 200, PROJ_H - 120, 400, 80)
                pygame.draw.rect(screen, (60, 120, 60), btn)
                pygame.draw.rect(screen, (100, 200, 100), btn, 4)
                next_text = font_btn.render("Next", True, (255, 255, 255))
                screen.blit(next_text, (btn.centerx - next_text.get_width() // 2, btn.centery - next_text.get_height() // 2))

            elif state == "solving":
                H_val = solve_homography(src_pts, DST_PTS)
                if H_val is not None:
                    H_solved = H_val
                    out_path = Path(config_dir) / "calibration.yaml"
                    save_calibration(out_path, H_val, (0, 0, PROJ_W, PROJ_H), (PROJ_W, PROJ_H))
                    state = "validate_1"
                else:
                    text = font_large.render("Homography failed. Restart calibration.", True, (255, 100, 100))
                    screen.blit(text, (PROJ_W // 2 - text.get_width() // 2, PROJ_H // 2 - 40))
                    state = "quit"

            elif state == "validate_1":
                # Draw grid and center target
                for i in range(4):
                    x = PROJ_W * (i + 1) // 4
                    pygame.draw.line(screen, (80, 80, 100), (x, 0), (x, PROJ_H), 2)
                for i in range(4):
                    y = PROJ_H * (i + 1) // 4
                    pygame.draw.line(screen, (80, 80, 100), (0, y), (PROJ_W, y), 2)
                cx, cy = int(PROJ_W / 2), int(PROJ_H / 2)
                pygame.draw.circle(screen, (255, 255, 0), (cx, cy), 25, 4)
                text = font_large.render("Tap the CENTER dot, then Next", True, (255, 255, 255))
                screen.blit(text, (PROJ_W // 2 - text.get_width() // 2, 80))
                if last_pointer is not None:
                    # Scale camera coords to projector (display) coords for feedback
                    px = int(last_pointer[0] * PROJ_W / w)
                    py = int(last_pointer[1] * PROJ_H / h)
                    pygame.draw.circle(screen, (0, 255, 0), (px, py), 15, 3)
                btn = pygame.Rect(PROJ_W // 2 - 200, PROJ_H - 120, 400, 80)
                pygame.draw.rect(screen, (60, 120, 60), btn)
                next_text = font_btn.render("Next", True, (255, 255, 255))
                screen.blit(next_text, (btn.centerx - next_text.get_width() // 2, btn.centery - next_text.get_height() // 2))

            elif state == "validate_2":
                for i in range(4):
                    x = PROJ_W * (i + 1) // 4
                    pygame.draw.line(screen, (80, 80, 100), (x, 0), (x, PROJ_H), 2)
                for i in range(4):
                    y = PROJ_H * (i + 1) // 4
                    pygame.draw.line(screen, (80, 80, 100), (0, y), (PROJ_W, y), 2)
                tlx, tly = int(PROJ_W / 4), int(PROJ_H / 4)
                pygame.draw.circle(screen, (255, 255, 0), (tlx, tly), 25, 4)
                text = font_large.render("Tap the TOP-LEFT dot, then Next", True, (255, 255, 255))
                screen.blit(text, (PROJ_W // 2 - text.get_width() // 2, 80))
                if last_pointer is not None:
                    # Scale camera coords to projector (display) coords for feedback
                    px = int(last_pointer[0] * PROJ_W / w)
                    py = int(last_pointer[1] * PROJ_H / h)
                    pygame.draw.circle(screen, (0, 255, 0), (px, py), 15, 3)
                btn = pygame.Rect(PROJ_W // 2 - 200, PROJ_H - 120, 400, 80)
                pygame.draw.rect(screen, (60, 120, 60), btn)
                next_text = font_btn.render("Next", True, (255, 255, 255))
                screen.blit(next_text, (btn.centerx - next_text.get_width() // 2, btn.centery - next_text.get_height() // 2))

            elif state == "done":
                if H_solved is not None and len(val_pts) >= 2:
                    import math
                    errs = []
                    for i, (cpx, cpy) in enumerate(val_pts):
                        if i < len(val_expected):
                            ppx, ppy = apply_homography(H_solved, cpx, cpy)
                            ex, ey = val_expected[i]
                            errs.append(math.hypot(ppx - ex, ppy - ey))
                    error_px = sum(errs) / len(errs) if errs else 0.0
                else:
                    error_px = None
                text = font_large.render("Calibration complete.", True, (200, 255, 200))
                screen.blit(text, (PROJ_W // 2 - text.get_width() // 2, 100))
                if error_px is not None:
                    err_text = font_large.render(f"Median error: {error_px:.1f} px", True, (255, 255, 200))
                    screen.blit(err_text, (PROJ_W // 2 - err_text.get_width() // 2, 200))
                done_btn = pygame.Rect(PROJ_W // 2 - 200, PROJ_H - 120, 400, 80)
                pygame.draw.rect(screen, (60, 120, 60), done_btn)
                done_text = font_btn.render("Done", True, (255, 255, 255))
                screen.blit(done_text, (done_btn.centerx - done_text.get_width() // 2, done_btn.centery - done_text.get_height() // 2))

            if state == "quit":
                break
            pygame.display.flip()
            clock.tick(30)
    finally:
        capture.release()
        pygame.quit()
