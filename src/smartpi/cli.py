"""Smart Pi Projector CLI. Commands: run, calibrate, healthcheck, bom.

Pipeline: Capture (Pi Camera or Wii Remote, IR pen) → Process (OpenCV, 4-point
auto-calibration) → Interact (OS-level mouse events, Kiosk web UI).
"""

from __future__ import annotations

from pathlib import Path

import click
import yaml

from smartpi import __version__


def _load_app_config(config_dir: str = "configs") -> dict:
    """Load configs/app.yaml merged with profile if present."""
    config_path = Path(config_dir) / "app.yaml"
    if not config_path.exists():
        return {"camera_index": 0, "resolution": [640, 480], "detector": "bright", "threshold": 200}
    with open(config_path) as f:
        app = yaml.safe_load(f) or {}
    profile_name = app.get("profile", "classroom")
    profile_path = Path(config_dir) / "profiles" / f"{profile_name}.yaml"
    if profile_path.exists():
        with open(profile_path) as pf:
            profile = yaml.safe_load(pf) or {}
        profile.pop("profile", None)
        app = {**app, **profile}
    return app


@click.group()
@click.version_option(version=__version__, prog_name="smartpi")
def main() -> None:
    """Smart Pi Projector — run, calibrate, healthcheck, bom."""
    pass


@main.command()
@click.option("--fullscreen", is_flag=True, help="Run in fullscreen (kiosk mode).")
@click.option("--config-dir", type=click.Path(exists=True, file_okay=False), default="configs")
def run(fullscreen: bool, config_dir: str) -> None:
    """Run the interactive projection app."""
    from smartpi.core.logging_config import configure_logging
    configure_logging(config_dir)
    try:
        from smartpi.renderer.pygame_app import run_app
        run_app(fullscreen=fullscreen, config_dir=config_dir)
    except ImportError as e:
        click.echo(f"Run requires renderer (Phase 6): {e}", err=True)
        raise SystemExit(1)


@main.command()
@click.option("--config-dir", type=click.Path(exists=True, file_okay=False), default="configs")
def calibrate(config_dir: str) -> None:
    """Run the calibration wizard."""
    from smartpi.core.logging_config import configure_logging
    configure_logging(config_dir)
    try:
        from smartpi.ui.calibration_wizard import run_wizard
        run_wizard(config_dir=config_dir)
    except ImportError as e:
        click.echo(f"Calibrate requires UI (Phase 5): {e}", err=True)
        raise SystemExit(1)


@main.command("export-diagnostics")
@click.option("--output", "-o", type=click.Path(), default="diagnostics_bundle.tar.gz", help="Output .tar.gz path.")
@click.option("--config-dir", type=click.Path(exists=True, file_okay=False), default="configs")
@click.option("--no-config", is_flag=True, help="Exclude config files from bundle.")
def export_diagnostics(output: str, config_dir: str, no_config: bool) -> None:
    """Bundle system info and config (excluding secrets) for bug reports."""
    from smartpi.core.logging_config import configure_logging
    configure_logging(config_dir)
    from smartpi.core.diagnostics import bundle_diagnostics
    path = bundle_diagnostics(output, include_config=not no_config, config_dir=config_dir)
    click.echo(f"Diagnostics written to {path}")


@main.command()
@click.option("--config-dir", type=click.Path(exists=True, file_okay=False), default="configs")
def healthcheck(config_dir: str) -> None:
    """Print system health (display, camera, FPS)."""
    from smartpi.core.logging_config import configure_logging
    configure_logging(config_dir)
    app_config = _load_app_config(config_dir)
    cam_index = app_config.get("camera_index", 0)
    res = app_config.get("resolution", [640, 480])
    w = res[0] if len(res) > 0 else 640
    h = res[1] if len(res) > 1 else 480

    import cv2
    cap = cv2.VideoCapture(cam_index)
    if not cap.isOpened():
        click.echo("FAIL: Camera not detected.")
        raise SystemExit(1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
    # Measure FPS over a few frames
    from smartpi.core.timing import FPSCounter
    fps_counter = FPSCounter(window_size=30)
    for _ in range(30):
        ret, _ = cap.read()
        if not ret:
            break
        fps_counter.tick()
    cap.release()
    fps = fps_counter.fps()
    click.echo("PASS: Camera detected.")
    click.echo(f"Resolution: {w}x{h}")
    click.echo(f"FPS: {fps:.1f}")
    # CPU temp on Pi
    try:
        with open("/sys/class/thermal/thermal_zone0/temp") as f:
            temp_millideg = int(f.read().strip())
        click.echo(f"CPU temp: {temp_millideg / 1000:.1f} C")
    except Exception:
        pass


@main.command()
@click.option(
    "--repo",
    type=click.Path(exists=True, file_okay=False),
    default=".",
    help="Repository root (directory containing hardware/).",
)
@click.option("--pen", is_flag=True, help="Also print IR pen BOM (hardware/ir_pen/pen_bom.csv).")
def bom(repo: str, pen: bool) -> None:
    """Print the bill of materials (main BOM and optionally IR pen BOM) from CSV."""
    from smartpi.core.bom import load_main_bom, load_pen_bom

    repo_path = Path(repo)
    try:
        rows = load_main_bom(repo_path)
    except FileNotFoundError as e:
        click.echo(f"Main BOM not found: {e}", err=True)
        raise SystemExit(1)
    click.echo("Main BOM (hardware/bom.csv):")
    if not rows:
        click.echo("  (empty)")
    else:
        for r in rows:
            part = r.get("part", "")
            qty = r.get("quantity", "")
            notes = r.get("notes", "")
            click.echo(f"  {part} x{qty} — {notes}")
    if pen:
        try:
            pen_rows = load_pen_bom(repo_path)
            click.echo("\nIR pen BOM (hardware/ir_pen/pen_bom.csv):")
            if not pen_rows:
                click.echo("  (empty)")
            else:
                for r in pen_rows:
                    part = r.get("part", "")
                    qty = r.get("quantity", "")
                    notes = r.get("notes", "")
                    click.echo(f"  {part} x{qty} — {notes}")
        except FileNotFoundError as e:
            click.echo(f"\nPen BOM not found: {e}", err=True)
