"""Load projector profile YAML from hardware/projector_profiles/. Optional; not required for capture."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def load_projector_profile(repo_root: str | Path, profile_name: str) -> dict[str, Any] | None:
    """Load a projector profile from hardware/projector_profiles/<profile_name>.yaml.

    Profiles typically contain resolution [w, h] and refresh_hint (Hz). The app does not
    load these by default; use this when you want to apply a projector preset (e.g. for
    display size or calibration).

    Args:
        repo_root: Directory containing the hardware/ folder.
        profile_name: Base name of the profile file (e.g. "generic_1080p" for generic_1080p.yaml).

    Returns:
        Dict with keys such as resolution, refresh_hint, or None if file missing/invalid.
    """
    path = Path(repo_root) / "hardware" / "projector_profiles" / f"{profile_name}.yaml"
    if not path.exists():
        return None
    try:
        import yaml
        with open(path) as f:
            data = yaml.safe_load(f)
        return data if isinstance(data, dict) else None
    except Exception:
        return None
