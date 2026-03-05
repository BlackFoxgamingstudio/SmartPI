"""Tests for BOM CSV loading (load_bom, load_main_bom, load_pen_bom) and CLI bom command."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

# Load bom module directly so tests don't require cv2 (core/__init__.py pulls in capture).
_REPO_ROOT = Path(__file__).resolve().parent.parent
_BOM_PATH = _REPO_ROOT / "src" / "smartpi" / "core" / "bom.py"


def _get_bom_module():
    spec = importlib.util.spec_from_file_location("smartpi.core.bom", _BOM_PATH)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load bom module from {_BOM_PATH}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_load_bom_returns_list_of_dicts(tmp_path):
    """load_bom parses a CSV and returns a list of dicts with header keys."""
    csv_path = tmp_path / "bom.csv"
    csv_path.write_text(
        "part,part_number_or_model,quantity,supplier,notes\n"
        "Raspberry Pi 4,RPi4-4GB,1,Official,4GB+ RAM\n"
        "HDMI cable,HDMI male-male,1,Retail,Pi to projector\n",
        encoding="utf-8",
    )
    bom = _get_bom_module()
    load_bom = bom.load_bom

    rows = load_bom(csv_path)
    assert len(rows) == 2
    assert rows[0]["part"] == "Raspberry Pi 4"
    assert rows[0]["quantity"] == "1"
    assert rows[0]["notes"] == "4GB+ RAM"
    assert rows[1]["part"] == "HDMI cable"


def test_load_bom_raises_file_not_found():
    """load_bom raises FileNotFoundError for missing path."""
    bom = _get_bom_module()
    with pytest.raises(FileNotFoundError, match="BOM file not found"):
        bom.load_bom(Path("/nonexistent/bom.csv"))


def test_load_bom_empty_file_returns_empty_list(tmp_path):
    """load_bom on a CSV with only headers returns empty list."""
    csv_path = tmp_path / "empty.csv"
    csv_path.write_text("part,quantity,notes\n", encoding="utf-8")
    bom = _get_bom_module()
    rows = bom.load_bom(csv_path)
    assert rows == []


def test_load_main_bom_repo_root():
    """load_main_bom(repo_root) loads hardware/bom.csv and returns expected columns."""
    repo_root = _REPO_ROOT
    bom_path = repo_root / "hardware" / "bom.csv"
    if not bom_path.exists():
        pytest.skip("hardware/bom.csv not found (run from repo root)")
    bom = _get_bom_module()
    rows = bom.load_main_bom(repo_root)
    assert len(rows) >= 1
    first = rows[0]
    assert "part" in first
    assert "quantity" in first
    # Optional columns in main BOM
    assert "part_number_or_model" in first or "notes" in first


def test_load_pen_bom_repo_root():
    """load_pen_bom(repo_root) loads hardware/ir_pen/pen_bom.csv."""
    repo_root = _REPO_ROOT
    pen_path = repo_root / "hardware" / "ir_pen" / "pen_bom.csv"
    if not pen_path.exists():
        pytest.skip("hardware/ir_pen/pen_bom.csv not found")
    bom = _get_bom_module()
    rows = bom.load_pen_bom(repo_root)
    assert len(rows) >= 1
    assert "part" in rows[0]
    assert "quantity" in rows[0]
    assert "notes" in rows[0]


def test_load_main_bom_raises_when_missing():
    """load_main_bom raises FileNotFoundError when hardware/bom.csv does not exist."""
    bom = _get_bom_module()
    with pytest.raises(FileNotFoundError, match="BOM file not found"):
        bom.load_main_bom(Path("/nonexistent/repo"))


def test_cli_bom_command():
    """CLI 'bom' command runs and prints main BOM (from repo root). Requires full env (smartpi + deps)."""
    pytest.importorskip("cv2", reason="CLI test needs full package (cv2)")
    from click.testing import CliRunner
    from smartpi.cli import main

    runner = CliRunner()
    repo_root = _REPO_ROOT
    result = runner.invoke(main, ["bom", "--repo", str(repo_root)])
    if (repo_root / "hardware" / "bom.csv").exists():
        assert result.exit_code == 0
        assert "Main BOM" in result.output or "bom.csv" in result.output
        assert "Raspberry" in result.output or "Pi" in result.output or "part" in result.output
    else:
        assert result.exit_code != 0
        assert "not found" in result.output.lower() or "BOM" in result.output


def test_cli_bom_command_with_pen():
    """CLI 'bom --pen' runs and includes pen BOM when file exists. Requires full env."""
    pytest.importorskip("cv2", reason="CLI test needs full package (cv2)")
    from click.testing import CliRunner
    from smartpi.cli import main

    runner = CliRunner()
    repo_root = _REPO_ROOT
    result = runner.invoke(main, ["bom", "--repo", str(repo_root), "--pen"])
    if (repo_root / "hardware" / "bom.csv").exists():
        assert result.exit_code == 0
    if (repo_root / "hardware" / "ir_pen" / "pen_bom.csv").exists():
        assert "pen" in result.output.lower() or "IR" in result.output
