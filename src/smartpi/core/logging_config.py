"""Load configs/logging.yaml and configure Python logging. No secrets in format."""

from __future__ import annotations

import logging
from pathlib import Path


_configured: bool = False


def configure_logging(config_dir: str | Path = "configs") -> None:
    """Load logging.yaml from config_dir and set root logger level and optional file handler.

    If the file is missing or invalid, logging is left at default (WARNING). No secrets
    are included in the log format. Idempotent: only configures once per process.
    """
    global _configured
    if _configured:
        return
    config_dir = Path(config_dir)
    path = config_dir / "logging.yaml"
    if not path.exists():
        return
    try:
        import yaml
        with open(path) as f:
            data = yaml.safe_load(f)
        if not data or not isinstance(data, dict):
            return
        level_name = (data.get("level") or "INFO").upper()
        level = getattr(logging, level_name, logging.INFO)
        logging.basicConfig(
            level=level,
            format="%(asctime)s %(levelname)s %(name)s: %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S",
        )
        root = logging.getLogger()
        root.setLevel(level)
        log_file = data.get("file")
        if log_file:
            try:
                fh = logging.FileHandler(log_file.strip(), encoding="utf-8")
                fh.setLevel(level)
                fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s", datefmt="%Y-%m-%dT%H:%M:%S"))
                root.addHandler(fh)
            except OSError:
                root.debug("Could not open log file %s", log_file)
        _configured = True
    except Exception:
        logging.getLogger(__name__).debug("Could not load logging config from %s", path, exc_info=True)
