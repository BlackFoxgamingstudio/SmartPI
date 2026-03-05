"""Send PointerEvents over WebSocket for web/remote clients."""

from __future__ import annotations

import json
import logging

from smartpi.interaction.events import PointerEvent

logger = logging.getLogger(__name__)


def send_pointer_event(ev: PointerEvent, socket: object) -> None:
    """Send a single PointerEvent over the given socket as JSON.

    Socket must provide send(data: bytes) or sendall(data: bytes). On send failure,
    logs the error and does not raise so one bad send does not kill the app.
    """
    payload = {
        "type": "pointer",
        "x": ev.x,
        "y": ev.y,
        "state": ev.state.value,
        "timestamp": ev.timestamp,
    }
    try:
        data = json.dumps(payload).encode("utf-8")
        if hasattr(socket, "send"):
            socket.send(data)
        elif hasattr(socket, "sendall"):
            socket.sendall(data)
        else:
            logger.warning("Socket has no send/sendall; cannot send pointer event")
    except (OSError, TypeError) as e:
        logger.debug("Failed to send pointer event: %s", e)
