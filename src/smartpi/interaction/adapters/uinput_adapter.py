"""Optional: emulate mouse/touch via Linux uinput. Requires evdev and root or uinput group."""

from __future__ import annotations

import logging
from typing import Any

from smartpi.interaction.events import PointerEvent, PointerState

logger = logging.getLogger(__name__)

_uinput_device: Any = None
_last_xy: tuple[float, float] | None = None


def _get_uinput():
    """Create or return cached uinput mouse device. Returns None if evdev missing or open fails."""
    global _uinput_device
    if _uinput_device is not None:
        return _uinput_device
    try:
        import evdev
        from evdev import UInput, ecodes
        capabilities = {
            ecodes.EV_REL: [ecodes.REL_X, ecodes.REL_Y],
            ecodes.EV_KEY: [ecodes.BTN_LEFT],
        }
        _uinput_device = UInput(capabilities, name="smartpi-virtual-mouse")
        return _uinput_device
    except ImportError:
        logger.debug("evdev not installed; uinput adapter is no-op. pip install evdev for mouse emulation.")
        return None
    except (OSError, PermissionError) as e:
        logger.debug("Could not create uinput device (need root or uinput group?): %s", e)
        return None


def emit_mouse(ev: PointerEvent, uinput_fd: int | None) -> None:
    """Emit a PointerEvent as a Linux uinput mouse event.

    If uinput_fd is None, uses a module-level virtual mouse (created on first call via evdev).
    A non-None uinput_fd is reserved for future use (currently ignored); pass None to use the
    auto-created device. Requires the evdev package and root or membership in the uinput group.
    On failure, logs and does not raise.
    """
    dev = _get_uinput() if uinput_fd is None else None
    if dev is None and uinput_fd is None:
        return
    if dev is None:
        logger.debug("uinput fd provided but evdev device not used; pass None to use auto-created device")
        return
    global _last_xy
    try:
        from evdev import ecodes
        if ev.state == PointerState.DOWN:
            dev.write(ecodes.EV_KEY, ecodes.BTN_LEFT, 1)
            dev.syn()
            _last_xy = (ev.x, ev.y)
        elif ev.state == PointerState.UP:
            dev.write(ecodes.EV_KEY, ecodes.BTN_LEFT, 0)
            dev.syn()
            _last_xy = None
        elif ev.state == PointerState.MOVE:
            if _last_xy is not None:
                dx = int(round(ev.x - _last_xy[0]))
                dy = int(round(ev.y - _last_xy[1]))
                if dx != 0 or dy != 0:
                    dev.write(ecodes.EV_REL, ecodes.REL_X, dx)
                    dev.write(ecodes.EV_REL, ecodes.REL_Y, dy)
                    dev.syn()
            _last_xy = (ev.x, ev.y)
    except (OSError, AttributeError) as e:
        logger.debug("uinput write failed: %s", e)
