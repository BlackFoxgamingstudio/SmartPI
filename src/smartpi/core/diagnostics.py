"""System stats and log bundling for bug reports."""

from __future__ import annotations

import os
import platform
import subprocess
import tarfile
import time
from pathlib import Path


def get_system_info() -> dict[str, str]:
    """Return a dict of system info (OS, Python, etc.)."""
    return {
        "platform": platform.platform(),
        "python": platform.python_version(),
        "processor": platform.processor() or "unknown",
    }


def bundle_diagnostics(
    output_path: str | Path,
    include_config: bool = True,
    config_dir: str | Path = "configs",
) -> Path:
    """Bundle logs and config into a tarball for bug reports. Excludes secrets.

    Args:
        output_path: Path for the output .tar.gz file.
        include_config: Whether to include config files (calibration excluded).
        config_dir: Path to config directory.

    Returns:
        Resolved path to the created tarball.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(output_path, "w:gz") as tar:
        info = get_system_info()
        info["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        info_path = Path(output_path).parent / "system_info.txt"
        info_path.write_text("\n".join(f"{k}: {v}" for k, v in info.items()))
        tar.add(str(info_path), arcname="system_info.txt")
        info_path.unlink()
        if include_config:
            config_path = Path(config_dir)
            if config_path.exists():
                for f in config_path.rglob("*"):
                    if f.is_file() and "calibration.yaml" not in str(f):
                        tar.add(str(f), arcname=f"config/{f.relative_to(config_path)}")
    return output_path.resolve()
