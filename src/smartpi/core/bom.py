"""Load BOM (bill of materials) CSV files. Uses stdlib csv only.

The main BOM (hardware/bom.csv) supports the Starter Kit (~$215) and the
hardware stack: Brain (Pi 5 4GB), Bridge (micro-HDMI to VGA + 3.5mm),
Tracker (Pi Camera v3 or Wii Remote), Muscle (surplus projector), Input (IR pen).
See project docs (e.g. docs/01_bill_of_materials.md).
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


def load_bom(path: str | Path) -> list[dict[str, Any]]:
    """Load a BOM CSV file and return a list of row dicts (keys = column names).

    The CSV is opened with utf-8 encoding and parsed with csv.DictReader.
    All values are strings; no type conversion is applied.

    Args:
        path: Path to the CSV file (e.g. hardware/bom.csv or hardware/ir_pen/pen_bom.csv).

    Returns:
        List of dicts, one per data row. Keys are the header column names.

    Raises:
        FileNotFoundError: If path does not exist.
        OSError: If the file cannot be read.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"BOM file not found: {path}")
    rows: list[dict[str, Any]] = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames:
            for row in reader:
                rows.append(dict(row))
    return rows


def load_pen_bom(repo_root: str | Path = ".") -> list[dict[str, Any]]:
    """Load the IR pen BOM CSV (hardware/ir_pen/pen_bom.csv) relative to repo root.

    Args:
        repo_root: Directory that contains the hardware/ folder (default: current dir).

    Returns:
        List of row dicts from pen_bom.csv (columns typically: part, quantity, notes).

    Raises:
        FileNotFoundError: If hardware/ir_pen/pen_bom.csv does not exist under repo_root.
    """
    path = Path(repo_root) / "hardware" / "ir_pen" / "pen_bom.csv"
    return load_bom(path)


def load_main_bom(repo_root: str | Path = ".") -> list[dict[str, Any]]:
    """Load the main BOM CSV (hardware/bom.csv) relative to repo root.

    Args:
        repo_root: Directory that contains the hardware/ folder (default: current dir).

    Returns:
        List of row dicts from bom.csv (columns: part, part_number_or_model, quantity, supplier, notes).

    Raises:
        FileNotFoundError: If hardware/bom.csv does not exist under repo_root.
    """
    path = Path(repo_root) / "hardware" / "bom.csv"
    return load_bom(path)
