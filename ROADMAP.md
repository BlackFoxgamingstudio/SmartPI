# Roadmap

This roadmap describes how the Smart Pi Interactive Projection project will evolve from hackathon demo to community kit.

## v0.1 — Hackathon Demo

**Goal:** Single-pointer interactive projection that runs on Pi + projector + camera.

- [x] Single pointer tracking (IR pen or bright spot)
- [x] Homography calibration (4-corner flow)
- [x] At least 2 scenes (Sandbox Draw, Particle Field)
- [x] Kiosk run script + build guide
- [x] Basic healthcheck and install scripts

**Definition of done:** Power on Pi + projector → app autostarts → calibrate in &lt; 2 min → draw and interact with particles; repo has BOM, build guide, and “how to add a scene.”

---

## v0.2 — Workshop Ready

**Goal:** Reliable for workshops and classrooms; easier to debug.

- [ ] Better lighting robustness (saved profiles: classroom, daylight, dark)
- [ ] Diagnostics bundle for bug reports (export_diagnostics.sh)
- [ ] More stable autostart + optional watchdog restart
- [ ] Documentation site (e.g. MkDocs) for easier onboarding

---

## v0.3 — Multi-touch / Multi-pointer

**Goal:** Support multiple pointers and richer gestures.

- [ ] Multi-blob tracking
- [ ] Gesture recognition (pinch, rotate)
- [ ] Improved UI composition (layered widgets)

---

## v1.0 — Community Kit

**Goal:** Replicable “kit” others can build and extend.

- [ ] Hardware kits: mounts, IR pen v2, compatibility matrix
- [ ] Full documentation site and “repair-forward” surplus projector field guide
- [ ] Clear compatibility matrix (projectors, cameras, Pi models)

---

**Last updated:** 2025-03-04
