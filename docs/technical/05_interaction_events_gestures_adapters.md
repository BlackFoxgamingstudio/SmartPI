# Interaction: Events, Gestures, and Adapters — Logic and Data In/Out

This document describes the interaction layer of Smart Pi: the pointer event model, gesture classification, event emission from the track stream, and the adapters that deliver events to Pygame (and optionally WebSocket or uinput). Every data structure, function input/output, and the logic that turns (xy, prev_xy, prev_down) into PointerEvents and then into scene or external consumer format are covered.

## Role of the interaction layer

The vision pipeline produces a stream of “current pointer position or None” each frame. The interaction layer turns this into a stream of **PointerEvents** (down, move, up) in projector space, with timestamps. Optionally, gestures (tap, drag, long_press) can be classified from short event sequences. Adapters then convert PointerEvents into the format expected by the consumer: the Pygame app uses a dict (type, x, y, state, timestamp); WebSocket would send serialized events; uinput would emit OS-level mouse events. The WebSocket adapter sends JSON over a socket; the uinput adapter emits OS-level mouse events via evdev when available. The Pygame adapter is used by the main app.

## Data structures: PointerState and PointerEvent

**Module:** `smartpi.interaction.events`

**PointerState:** Enum with values `DOWN`, `MOVE`, `UP`. Represents the semantic state of the pointer in a single event.

**PointerEvent:** Dataclass with:
- `x` (float): projector-space x.
- `y` (float): projector-space y.
- `state` (PointerState): DOWN, MOVE, or UP.
- `timestamp` (float): from `time.perf_counter()` when the event was created.
- `confidence` (float): default 1.0; optional detection confidence (not currently set by the pipeline).

**Data in/out:** These are output types of the gesture layer and input types to the adapters. No functions “take” PointerState as input except for comparison in gesture logic; PointerEvent is created in `emit_events_from_track` and consumed by adapters and (after conversion) by scenes.

---

## Event emission: `emit_events_from_track(xy, prev_xy, prev_down)`

**Module:** `smartpi.interaction.gesture`

**Purpose:** Yield zero or more PointerEvents for the current frame given the current pointer position (or None) and the previous frame’s position and “down” state. The caller (main app) is responsible for maintaining prev_xy and prev_down across frames.

**Inputs:**
- `xy` (tuple[float, float] | None): current smoothed pointer position in projector space, or None if pointer was not detected this frame.
- `prev_xy` (tuple[float, float] | None): previous frame’s position (or None if pointer was not down last frame).
- `prev_down` (bool): whether the pointer was considered “down” in the previous frame (i.e. we had a valid position last frame).

**Outputs:** Iterator of `PointerEvent`. Events are yielded in order for this frame only; the caller iterates and forwards each to the scene/adapter.

**Logic:**
1. `t = time.perf_counter()` (timestamp for all events this frame).
2. If `xy is None`: if `prev_down` is True, yield one `PointerEvent(prev_xy[0], prev_xy[1], PointerState.UP, t)`. Then return (no more events). So “pointer lost” generates an UP at the last known position.
3. If `xy is not None`:  
   - If `prev_xy is None` and not `prev_down`: yield `PointerEvent(xy[0], xy[1], PointerState.DOWN, t)` (pointer appeared).  
   - Else if `prev_xy is not None` and (xy[0] != prev_xy[0] or xy[1] != prev_xy[1]): yield `PointerEvent(xy[0], xy[1], PointerState.MOVE, t)` (pointer moved).  
   - No explicit UP when pointer is still present; UP is only when xy becomes None.

So the state machine is: no pointer → DOWN when pointer appears; pointer present → MOVE when position changes; pointer present → (no event) when position unchanged; pointer lost → UP. The main app then sets `prev_xy = pointer` (or None) and `prev_down = (pointer is not None)` for the next frame.

---

## Gesture classification: `classify_gesture(events) -> str`

**Module:** `smartpi.interaction.gesture`

**Purpose:** Classify a short sequence of PointerEvents (e.g. from down to up) as `"tap"`, `"drag"`, `"long_press"`, or `"none"`. Used when higher-level logic needs to distinguish tap from drag or long-press (e.g. for context menus or different scene actions).

**Inputs:** `events`: list of PointerEvent, typically in time order (down, optional moves, up).

**Outputs:** One of the strings `"tap"`, `"drag"`, `"long_press"`, `"none"`.

**Logic:**
- If list is empty, return `"none"`.
- Require at least one DOWN and one UP; otherwise return `"none"`.
- Find the DOWN event and the last UP event; compute `dt = up.timestamp - down.timestamp` and distance between down and up positions: `dist = sqrt((up.x - down.x)^2 + (up.y - down.y)^2)`.
- Constants: `TAP_TIME_THRESHOLD = 0.3` s, `TAP_DISTANCE_THRESHOLD = 20.0` px, `LONG_PRESS_TIME = 0.5` s.
- If `dt >= LONG_PRESS_TIME`: return `"long_press"`.
- If `dist > TAP_DISTANCE_THRESHOLD` or number of MOVE events > 2: return `"drag"`.
- Else return `"tap"`.

So tap = short in time and small in distance with few moves; long_press = held long; drag = moved too far or too many moves. The main app does not currently call `classify_gesture` in the loop; scenes receive raw down/move/up and can implement their own logic or call this on a collected buffer if needed.

---

## Pygame adapter: `pygame_event_from_pointer(ev)` and `push_to_pygame(ev, callback)`

**Module:** `smartpi.interaction.adapters.pygame_adapter`

**pygame_event_from_pointer(ev):**  
- **Input:** One `PointerEvent`.  
- **Output:** Dict with keys: `"type"` (string `"pointer"`), `"x"` (float), `"y"` (float), `"state"` (string: `ev.state.value`, i.e. `"down"`, `"move"`, `"up"`), `"timestamp"` (float).  
- **Logic:** Build and return the dict. This is the format that scenes expect in `on_pointer(ev)`.

**push_to_pygame(ev, callback):**  
- **Input:** PointerEvent and a callable `callback` that accepts one dict (the pygame-style event).  
- **Output:** None.  
- **Logic:** `callback(pygame_event_from_pointer(ev))`. So it is a convenience: convert and push in one call. The main app could instead call `pygame_event_from_pointer` and then `scene.on_pointer(...)` directly, which it does: it does not use `push_to_pygame` but uses `pygame_event_from_pointer(ev)` and passes the result to `scene.on_pointer(...)`.

---

## WebSocket and uinput adapters (implemented)

**WebSocket:** `send_pointer_event(ev, socket)` — Serializes the PointerEvent to JSON (`type`, `x`, `y`, `state`, `timestamp`) and sends it via `socket.send(data)` or `socket.sendall(data)`. On failure, logs and does not raise. **Data in:** PointerEvent, socket-like object. **Data out:** None.

**uinput:** `emit_mouse(ev, uinput_fd)` — Emits Linux mouse events via the evdev library when available (requires `pip install evdev` and root or uinput group). If `uinput_fd` is `None`, uses an auto-created virtual mouse device; a non-None `uinput_fd` is reserved for future use (currently ignored). Maps DOWN/UP to BTN_LEFT press/release and MOVE to REL_X/REL_Y. **Data in:** PointerEvent, optional fd. **Data out:** None.

---

## End-to-end flow in the main app

1. After tracker update: `pointer = (smooth_x, smooth_y)` or `pointer = None`; app has `prev_xy` and `prev_down` from last frame.
2. `for ev in emit_events_from_track(pointer, prev_xy, prev_down):` — iterate events for this frame.
3. For each ev: if scene has `on_pointer`, call `scene.on_pointer(pygame_event_from_pointer(ev))`.
4. Update state: if pointer is not None, set `prev_xy = pointer`, `prev_down = True`; else `prev_xy = None`, `prev_down = False`.

So the **input** to the interaction layer each frame is (xy, prev_xy, prev_down). The **output** is a sequence of PointerEvents, each converted to a dict and passed to the active scene. No gesture classification is done in the default loop unless a scene buffers events and calls `classify_gesture` itself.

---

## Summary: data in and out

| Function / type           | Data in                          | Data out                    |
|---------------------------|----------------------------------|-----------------------------|
| PointerEvent              | (constructed with x,y,state,t)   | N/A                         |
| emit_events_from_track    | xy, prev_xy, prev_down           | Iterator[PointerEvent]      |
| classify_gesture          | list[PointerEvent]               | "tap"\|"drag"\|"long_press"\|"none" |
| pygame_event_from_pointer | PointerEvent                     | dict (type,x,y,state,timestamp) |
| push_to_pygame            | PointerEvent, callback           | None                        |

The next document covers the renderer (main loop, scenes, overlay) and the calibration wizard and CLI/operations.

Last updated: 2025-03-04
