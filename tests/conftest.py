"""Pytest fixtures: sample frame paths, mock config."""

import pytest


@pytest.fixture
def config_dir(tmp_path):
    """A temporary config directory with app.yaml."""
    (tmp_path / "app.yaml").write_text(
        "camera_index: 0\nresolution: [640, 480]\ndetector: bright\nthreshold: 200\n"
    )
    (tmp_path / "profiles").mkdir()
    (tmp_path / "profiles" / "classroom.yaml").write_text("threshold: 180\nblur: 3\n")
    return str(tmp_path)


@pytest.fixture
def sample_frame_path():
    """Path to a minimal sample frame (optional; tests can skip if missing)."""
    from pathlib import Path
    p = Path(__file__).parent.parent / "data" / "samples" / "frames"
    if not p.exists():
        return None
    for ext in ("*.png", "*.jpg"):
        for f in p.glob(ext):
            return str(f)
    return None
