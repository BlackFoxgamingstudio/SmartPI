# Gaps and Implementation Status

This document tracks identified gaps (logic, documentation, assets, integration) and their implementation status so each can be driven to 100%.

**Last updated:** 2026-03-04

---

## 1. Chatbot (index.html)

| Gap | Status | Notes |
|-----|--------|--------|
| Duplicate Enter keydown handler causing double-send | **Fixed** | Removed second `input.addEventListener('keydown', ...)` that always called `sendBtn.click()`. Single handler now: if suggestions visible and highlight ≥ 0 → pick suggestion and reply; else → send current input. |
| Embedded CSV out of sync with handbook_chatbot.csv | **Process** | Embedded `<script id="handbook-csv">` must match CSV row count for file:// and fallback. Run `scripts/sync_chatbot_csv_to_index.py` after editing `handbook_chatbot.csv` to refresh the embedded block. |
| Best-answer scoring | **Documented** | `scoreRow` weights question tokens ×2, response tokens ×1; exact match preferred; `bestScore < 1` returns null. See inline comments in index.html. |

---

## 2. Handbook and documentation

| Gap | Status | Notes |
|-----|--------|--------|
| docs/10_event_and_venue_requirements.md not in handbook index | **Fixed** | Added to Documentation index in index.html. |
| docs/11_problem_and_value.md not in handbook index | **Fixed** | Added to Documentation index in index.html. |

---

## 3. Source code

| Gap | Status | Notes |
|-----|--------|--------|
| pygame_app _load_config merge profile | **Done** | `_load_config` in pygame_app.py merges `configs/profiles/<profile>.yaml` (already implemented). |
| Load configs/logging.yaml | **Done** | `smartpi.core.logging_config.configure_logging(config_dir)` loads logging.yaml; called from CLI and run_app. |
| WebSocket adapter serialize + send | **Done** | `send_pointer_event` serializes PointerEvent to JSON and sends via socket.send/sendall; logs on failure. |
| uinput adapter | **Done** | `emit_mouse` uses evdev UInput for relative mouse events; requires evdev and root/uinput group. |
| STEM widgets (ruler, angles, graph) | **Done** | stem_widgets.py implements ruler segments, angle triples with degrees, graph paper grid and snap. |

---

## 4. Hardware and assets

| Gap | Status | Notes |
|-----|--------|--------|
| hardware/enclosure/stl/ empty | **Documented** | README states: if stl/ is empty, use your own or community-shared enclosure STLs. |
| hardware/camera_mount/stl/ and cad/ empty | **Documented** | README states: if empty, use your own or community-shared mount STLs; cad/ for user edits. |
| hardware/ir_pen/wiring_diagram.svg placeholder | **Documented** | README states: "template only; replace or augment with your schematic" per pen_bom.csv. |
| hardware/projector_profiles/*.yaml | **Documented** | config_reference.md and api_overview.md describe optional use for display size when no calibration. |

---

## 5. Integration and process

| Gap | Status | Notes |
|-----|--------|--------|
| Single source for chatbot Q&A | **Process** | Source of truth: handbook_chatbot.csv. Embedded copy in index.html is refreshed by `scripts/sync_chatbot_csv_to_index.py`. |
| After generate_chatbot_qa.py | **Process** | After adding Q&A with the script, run `scripts/sync_chatbot_csv_to_index.py` so index.html has the same rows for file:// and fallback. |

---

## 6. Scripts

- **scripts/sync_chatbot_csv_to_index.py** — Reads `handbook_chatbot.csv` and updates the embedded `<script id="handbook-csv">` block in `index.html` so row count matches. Run from repo root after editing the CSV.

---

## Cross-references

- Incomplete logic audit (historical): `.cursor/plans/incomplete_logic_and_files_audit_464f4e1c.plan.md`
- Best practices checklist: [docs/00_best_practices.md](00_best_practices.md)
- API and technical deep dives: [docs/technical/README.md](technical/README.md), [api_overview.md](api_overview.md)
