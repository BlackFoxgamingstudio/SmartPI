Below is a research-informed open-source GitHub repo blueprint (file structure + architecture) and a detailed build plan for your hackathon demo and for evolving it into a repair-forward, replicable “Smart Pi Interactive Projection Experience.”

I’m anchoring the interaction stack on camera-based IR pen / bright-point tracking because it’s hardware-light and well-supported by prior art: TipTrack’s IR pen approach (Linux + projector + IR-sensitive camera)  ￼ plus well-known laser/bright-point tracking patterns that include calibration utilities  ￼. I’m also including a “projection mapping / calibration” lane that can grow into a full mapping SDK (Processing ecosystem, PapARt) if you later want spatialized content and more advanced geometry  ￼.

⸻

1) Reference architecture (what you’re building)

Physical system
	•	Compute: Raspberry Pi (Pi 4/5 preferred for OpenCV throughput; Pi Zero can “play content” but will struggle with low-latency vision).
	•	Display: Surplus projector (HDMI input).
	•	Sensing options (choose 1 for demo, keep both as roadmap):
	1.	IR-pen + IR camera (recommended): IR LED pen tip + IR-sensitive camera + (optional) IR-pass / visible-cut filter. TipTrack-style approach is proven for arbitrary surfaces.  ￼
	2.	Visible bright-point (laser/LED): Standard webcam tracking a bright point; easiest to source parts, less robust under varied lighting; still great for hackathon demo and calibration UX iterations.  ￼

Software system (pipelines)
	1.	Capture: Camera frames (libcamera / OpenCV)
	2.	Detect: Bright point / IR blob detection → candidate points
	3.	Track: Temporal smoothing + ID assignment (single-point first; multi-point later)
	4.	Calibrate: Map camera coordinates → projector coordinates (homography)
	5.	Interact: Convert projector coordinates → pointer events (touch-like)
	6.	Render: Display layer (fullscreen visuals) reacts to events
	7.	Operate: A “kiosk-like” launcher with health checks, FPS counters, and a fast “recalibrate” flow

Why this split matters
	•	You can swap detectors (IR pen vs laser vs colored marker) without touching UI apps.
	•	You can swap renderers (Pygame, Processing, Godot, Web) without touching calibration/tracking.
	•	You can ship a “minimal working demo” quickly, then harden each layer iteratively.

⸻

2) Best-practice open-source GitHub repo file structure

This structure is optimized for:
	•	fast hackathon onboarding,
	•	hardware replication,
	•	reproducible builds,
	•	calibration UX iteration,
	•	CI checks even when hardware isn’t present.

smart-pi-interactive-projection/
├─ README.md
├─ LICENSE
├─ CODE_OF_CONDUCT.md
├─ CONTRIBUTING.md
├─ SECURITY.md
├─ CITATION.cff
├─ CHANGELOG.md
├─ ROADMAP.md
├─ .gitignore
├─ .editorconfig
├─ pyproject.toml
├─ uv.lock                      # or poetry.lock / requirements.txt (choose one)
├─ requirements-dev.txt          # if not using lock-based tool
├─ Makefile
├─ docker/
│  ├─ Dockerfile.dev             # builds on Debian slim w/ OpenCV deps (x86 dev)
│  └─ compose.yaml               # optional: for dev tooling, not for Pi camera
├─ scripts/
│  ├─ install_pi.sh              # installs deps + sets up services
│  ├─ enable_kiosk.sh            # sets autostart + fullscreen
│  ├─ calibrate.sh               # runs calibration wizard
│  ├─ run_demo.sh                # runs end-to-end demo
│  ├─ healthcheck.sh             # checks camera, GPU, display, permissions
│  └─ export_diagnostics.sh      # bundles logs/config for bug reports
├─ docs/
│  ├─ 00_overview.md
│  ├─ 01_bill_of_materials.md
│  ├─ 02_build_guide.md
│  ├─ 03_repair_forward_notes.md
│  ├─ 04_system_architecture.md
│  ├─ 05_calibration_ux.md
│  ├─ 06_interaction_design.md
│  ├─ 07_troubleshooting.md
│  ├─ 08_safety_and_power.md
│  ├─ 09_accessibility_and_inclusion.md
│  ├─ images/
│  ├─ diagrams/
│  │  ├─ architecture.mmd        # mermaid sources
│  │  └─ calibration_flow.mmd
│  └─ demo_walkthrough/
│     ├─ showcase_script.md
│     └─ operator_checklist.md
├─ hardware/
│  ├─ bom.csv                    # canonical part list, vendor-agnostic
│  ├─ projector_profiles/
│  │  ├─ generic_1080p.yaml
│  │  └─ your_projector_model.yaml
│  ├─ camera_mount/
│  │  ├─ stl/                    # printable mounts
│  │  ├─ cad/                    # source CAD
│  │  └─ README.md
│  ├─ ir_pen/
│  │  ├─ wiring_diagram.svg
│  │  ├─ pen_bom.csv
│  │  └─ README.md
│  └─ enclosure/
│     ├─ stl/
│     └─ README.md
├─ configs/
│  ├─ app.yaml                   # global config (camera index, thresholds)
│  ├─ calibration.yaml           # stored homography + surface bounds
│  ├─ profiles/
│  │  ├─ classroom.yaml
│  │  ├─ dark_room.yaml
│  │  └─ daylight.yaml
│  └─ logging.yaml
├─ data/
│  ├─ samples/
│  │  ├─ frames/                 # sample frames for offline testing
│  │  └─ videos/                 # sample clips for regression tests
│  └─ calibration_runs/          # saved JSON/YAML from calibration sessions
├─ src/
│  └─ smartpi/
│     ├─ __init__.py
│     ├─ cli.py                  # `smartpi run`, `smartpi calibrate`, etc.
│     ├─ core/
│     │  ├─ capture.py           # camera abstraction
│     │  ├─ timing.py            # FPS, frame timing, performance counters
│     │  └─ diagnostics.py       # system stats + logs bundling
│     ├─ vision/
│     │  ├─ preprocess.py        # grayscale, blur, threshold, masks
│     │  ├─ detect_ir.py          # IR blob detector (threshold + morphology)
│     │  ├─ detect_bright.py      # visible bright spot detector
│     │  ├─ track.py             # smoothing + optional kalman
│     │  ├─ calibrate.py         # homography solve + persistence
│     │  └─ validate.py          # calibration sanity checks
│     ├─ interaction/
│     │  ├─ events.py            # normalized pointer events
│     │  ├─ gesture.py           # tap/hold/drag; multi-touch later
│     │  └─ adapters/
│     │     ├─ pygame_adapter.py
│     │     ├─ websocket_adapter.py
│     │     └─ uinput_adapter.py # optional: emulate mouse/touch events
│     ├─ renderer/
│     │  ├─ pygame_app.py         # default demo visuals
│     │  ├─ scenes/
│     │  │  ├─ sandbox_draw.py
│     │  │  ├─ particle_field.py
│     │  │  └─ stem_widgets.py
│     │  └─ assets/
│     │     ├─ audio/
│     │     └─ shaders/          # optional
│     ├─ ui/
│     │  ├─ calibration_wizard.py # guided flow, big buttons, minimal typing
│     │  └─ overlay.py            # debug overlay (FPS, thresholds, pointers)
│     └─ services/
│        ├─ systemd/
│        │  ├─ smartpi.service
│        │  └─ README.md
│        └─ autostart/
│           └─ smartpi.desktop
├─ tests/
│  ├─ test_calibration.py
│  ├─ test_tracking.py
│  ├─ test_configs.py
│  └─ fixtures/
├─ benchmarks/
│  ├─ bench_detector.py
│  └─ perf_notes.md
└─ .github/
   ├─ workflows/
   │  ├─ ci.yml                  # lint + unit tests + type checks
   │  ├─ release.yml             # builds tagged releases, bundles assets
   │  └─ docs.yml                # builds docs site (mkdocs)
   ├─ ISSUE_TEMPLATE/
   │  ├─ bug_report.yml
   │  ├─ feature_request.yml
   │  └─ hardware_compat.yml
   └─ PULL_REQUEST_TEMPLATE.md

Why these folders exist (the “repair-forward, replicable” rationale)
	•	hardware/ is first-class: mounts, wiring, projector profiles, BOMs, and “known-good setups.”
	•	configs/ separates environment tuning from code; this is critical for different rooms/surfaces.
	•	data/samples/ makes your tracking/calibration testable in CI without a camera connected.
	•	services/ enables kiosk-mode installs for workshops and classrooms.
	•	docs/ turns your hackathon demo into a replicable “kit” others can rebuild.

⸻

3) Core technical design choices (with research anchors)

Interaction tracking baseline: IR pen / bright-point tracking
	•	TipTrack / IRPenTracking demonstrates robust IR pen tracking with Linux + projector + IR-sensitive cameras; this is a strong conceptual anchor for your IR-pen mode and future “real interactive whiteboard” feel.  ￼
	•	Laser/bright point tracking projects show simpler approaches and include calibration and demo utilities; these are excellent references for quick demos and for designing your calibration UX.  ￼

Projection calibration baseline: homography
	•	A projector surface is a planar mapping problem: camera-space → projector-space is typically solved with a homography using 4+ point correspondences.
	•	SparkFun’s projection mapping tutorial material is a practical on-ramp for “CV + projection mapping” thinking and terminology, useful for your docs and onboarding.  ￼

Future lane: projection mapping SDK (optional)
	•	If your collaborators want “interactive mapped art installations,” Processing-based toolkits like PapARt are relevant prior art (interactive projection mapping SDK).  ￼
This is not the fastest path for the hackathon demo, but it’s a credible “Phase 2/3” growth path.

⸻

4) Detailed project plan (hackathon demo → open-source v1)

I’m laying this out as workstreams with milestones, acceptance criteria, and artifacts so the repo stays coherent even with many contributors.

Workstream A — System bring-up (Pi + projector + camera)

Goal: stable fullscreen output + stable camera frames + consistent startup.

Tasks
	1.	Flash Pi OS, enable SSH, GPU memory tuning, install deps (OpenCV, libcamera stack, SDL/Pygame).
	2.	Verify projector modes (720p/1080p), set fixed resolution, disable screen blanking.
	3.	Camera: lock exposure where possible; confirm frame rate (>= 30 FPS target).
	4.	Add scripts/healthcheck.sh that prints:
	•	display resolution
	•	camera device detected
	•	measured FPS
	•	CPU temp / throttling flags
	5.	Add kiosk launcher:
	•	smartpi run --fullscreen
	•	autostart via systemd or desktop autostart.

Acceptance criteria
	•	On boot, the Pi displays the demo app fullscreen within ~30–60 seconds.
	•	Healthcheck returns “PASS” for display + camera + basic FPS.

Repo artifacts
	•	scripts/install_pi.sh, services/systemd/smartpi.service, docs/02_build_guide.md

⸻

Workstream B — Detection + tracking (single point first)

Goal: detect a pointer point (IR pen tip or bright spot) and track it smoothly.

Tasks
	1.	Implement vision/detect_ir.py:
	•	grayscale → threshold → morphology → blob extraction
	2.	Implement vision/detect_bright.py:
	•	HSV/brightness threshold path for visible bright point
	3.	Implement vision/track.py:
	•	smoothing (EMA) + velocity clamp
	•	optional Kalman later
	4.	Debug overlay:
	•	show thresholded mask, detected point, FPS, current threshold values
	5.	Offline regression:
	•	store a handful of sample frames/videos in data/samples/
	•	create tests that verify detector returns reasonable coordinates

Acceptance criteria
	•	Pointer dot is consistently detected at ≥ 20 FPS (preferably ≥ 30 FPS).
	•	Cursor jitter is low enough to draw a legible line.

Research anchors
	•	Laser/bright-point trackers demonstrate calibration + demo structure patterns that you can mirror.  ￼
	•	IR pen tracking on arbitrary surfaces is established by TipTrack / IRPenTracking.  ￼

⸻

Workstream C — Calibration UX (camera → projector mapping)

Goal: calibration that a new user can complete in < 2 minutes.

Calibration flow (recommended for hackathon)
	1.	Project 4 corner targets (big, high-contrast).
	2.	User taps each target with the IR pen / pointer (or holds pointer steady).
	3.	Capture the pointer coordinates in camera space for each target.
	4.	Solve homography; persist to configs/calibration.yaml.
	5.	Validate: project a crosshair grid; user taps 1–2 verification points; compute error.

Tasks
	•	vision/calibrate.py: homography solve + persistence
	•	ui/calibration_wizard.py: big “Next” buttons, minimal typing
	•	vision/validate.py: compute reprojection error stats and warn if poor

Acceptance criteria
	•	After calibration, projected cursor aligns to pointer within a tolerable error band (define target: e.g., < 15 px median error at 1080p for demo; tighten later).
	•	Calibration artifacts saved and reload correctly at app start.

Research anchor
	•	Practical CV + projection mapping workflows are well documented in hobbyist/education contexts, helpful for explaining and teaching the calibration concept.  ￼

⸻

Workstream D — Interaction layer (events + gestures)

Goal: convert tracked points into usable interaction primitives.

Tasks
	1.	Define interaction/events.py:
	•	PointerEvent(x, y, state, timestamp, confidence)
	2.	Implement gesture.py:
	•	tap (down→up within threshold)
	•	drag (down + motion)
	•	long press (time threshold)
	3.	Adapter strategy:
	•	Pygame adapter for your built-in demo scenes
	•	Websocket adapter so others can build web visuals quickly
	•	Optional: Linux uinput adapter to emulate mouse events later

Acceptance criteria
	•	Drawing app works reliably: touch-down starts line, drag draws, lift ends stroke.
	•	Events stable under varying lighting profiles via configs/profiles/*.yaml.

⸻

Workstream E — Demo experience (showcase-ready)

Goal: “interactive projection experience” that is visually compelling in 30 seconds.

Recommended hackathon demo scenes (ship at least 2)
	1.	Sandbox Draw: IR pen draws ink; color palette toggles by corner hotzones.
	2.	Particle Field: pointer “pushes” particles; shows latency and delight.
	3.	(Optional) STEM Widgets: projected ruler/angles/graph paper; pointer snaps points.

Tasks
	•	Build renderer/pygame_app.py with a scene selector
	•	Add docs/demo_walkthrough/showcase_script.md
	•	Add an operator checklist: “boot → recalibrate → run scenes → exit”

Acceptance criteria
	•	A new operator can run the demo without touching code.
	•	Demo is stable for ≥ 10 minutes continuous runtime.

⸻

Workstream F — Documentation + open-source readiness

Goal: others can replicate, modify, and contribute.

Docs you should ship for v0.1
	•	docs/01_bill_of_materials.md: projector notes, camera, IR pen parts, mounts
	•	docs/02_build_guide.md: step-by-step setup
	•	docs/05_calibration_ux.md: calibration screenshots + troubleshooting
	•	docs/07_troubleshooting.md: “no camera,” “low FPS,” “bad alignment,” “lighting”
	•	docs/03_repair_forward_notes.md: how to source surplus projectors, common fixes

Repo hygiene
	•	CONTRIBUTING.md: how to run locally, how to add sample frames, code style
	•	.github/ISSUE_TEMPLATE/hardware_compat.yml: collect projector/camera compatibility
	•	CI: lint + unit tests + type checks (even if hardware tests are manual)

Acceptance criteria
	•	A stranger can follow the build guide and reach “demo running” without asking you in person.
	•	At least 1 outside collaborator can add a scene or a hardware profile cleanly.

⸻

5) Role-based contribution map (for hackathon collaboration)

To make the project “intentionally open-ended” without becoming chaotic, give each contributor a lane:
	1.	Hardware Rigging

	•	Camera mount, alignment, IR filter hack, cable management, transport case
	•	Output: hardware/camera_mount/*, hardware/enclosure/*, photos + notes

	2.	Calibration UX / Operator Experience

	•	Reduce steps, improve reliability, add “recalibrate quickly”
	•	Output: src/smartpi/ui/*, docs/05_calibration_ux.md

	3.	Vision + Tracking

	•	Improve detection robustness, performance, false positive rejection
	•	Output: src/smartpi/vision/*, benchmarks/*, data/samples/*

	4.	Creative Visuals / Sound

	•	New scenes; audio-reactive effects; collaboration tools
	•	Output: src/smartpi/renderer/scenes/*, src/smartpi/renderer/assets/*

	5.	Packaging + Installer

	•	install_pi.sh, system service, kiosk mode polish
	•	Output: scripts/*, src/smartpi/services/*

⸻

6) Practical “definition of done” for the showcase (demo-grade)

You’ll know you’ve hit the hackathon target when you can do this, live:
	1.	Power on Pi + projector.
	2.	App autostarts to a “Start / Calibrate / Demo” menu.
	3.	Run calibration in under 2 minutes.
	4.	Launch Sandbox Draw: the pointer draws where the pen touches.
	5.	Switch to Particle Field: the pointer interacts with physics.
	6.	Open the repo and show:
	•	BOM
	•	build guide
	•	“how calibration works”
	•	how to add a new scene

⸻

7) Suggested “Roadmap.md” phases (so the repo evolves cleanly)

v0.1 (Hackathon Demo)
	•	single pointer tracking
	•	homography calibration
	•	2 scenes
	•	kiosk run script + build guide

v0.2 (Workshop Ready)
	•	better lighting robustness
	•	saved profiles (classroom/daylight/dark)
	•	diagnostics bundle for bug reports
	•	more stable autostart + watchdog restart

v0.3 (Multi-touch / Multi-pointer)
	•	multi-blob tracking
	•	gesture recognition (pinch/rotate)
	•	improved UI composition (layered widgets)

v1.0 (Community Kit)
	•	hardware kits: mounts, IR pen v2, compatibility matrix
	•	documentation site (mkdocs)
	•	“repair-forward” surplus projector field guide

⸻

If you want, I can also produce the actual contents of the top-level repo docs (README, BOM template, build guide, calibration UX spec, contribution guide) in the exact tone and format you want for GitHub—ready to paste into files—without changing the structure above.