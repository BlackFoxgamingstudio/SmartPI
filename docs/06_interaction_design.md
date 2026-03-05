# Interaction Design

How tracked pointer positions become usable interaction primitives.

## PointerEvent

Normalized event emitted by the interaction layer:

- **x, y** — Projector-space coordinates (0–1 or pixel).
- **state** — e.g. down, move, up.
- **timestamp** — For gesture timing.
- **confidence** — Optional detection confidence.

## Gestures

- **Tap** — Pointer down then up within a short time and distance threshold.
- **Drag** — Pointer down followed by motion; emit move events until up.
- **Long press** — Down held for a time threshold (e.g. 500 ms).

Multi-touch (pinch, rotate) is planned for a later roadmap phase.

## Adapters

- **Pygame adapter** — Feeds events into the built-in Pygame demo scenes (Sandbox Draw, Particle Field).
- **WebSocket adapter** — Sends events over a socket so web or other clients can drive visuals.
- **uinput adapter** (optional) — Emulates mouse/touch events at the OS level on Linux.

Scenes receive events via the active adapter; swapping adapters does not require changing scene logic.

Last updated: 2025-03-04
