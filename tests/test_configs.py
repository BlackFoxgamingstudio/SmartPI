"""Tests for config loading."""

import pytest
import yaml
from pathlib import Path


def test_load_app_config(config_dir):
    """Load app.yaml from config_dir."""
    from smartpi.cli import _load_app_config
    config = _load_app_config(config_dir)
    assert "camera_index" in config
    assert config.get("resolution") == [640, 480]
    assert config.get("threshold") in (180, 200)  # may be overridden by profile


def test_calibration_example_schema():
    """Example calibration YAML has expected keys."""
    path = Path(__file__).parent.parent / "configs" / "calibration.yaml.example"
    if not path.exists():
        pytest.skip("calibration.yaml.example not found")
    with open(path) as f:
        data = yaml.safe_load(f)
    assert "homography" in data
    assert "bounds" in data
    assert "resolution" in data
    assert len(data["homography"]) == 3
