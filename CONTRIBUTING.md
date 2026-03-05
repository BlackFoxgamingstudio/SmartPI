# Contributing to Smart Pi Interactive Projection

Thank you for your interest in contributing. This document explains how to contribute and what we expect.

## Code of Conduct

By participating, you agree to uphold our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it first.

## Types of Contributions We Welcome

- **Bug reports** — Use the [bug report template](.github/ISSUE_TEMPLATE/bug_report.yml) when opening an issue.
- **Feature ideas** — Use the [feature request template](.github/ISSUE_TEMPLATE/feature_request.yml).
- **Hardware compatibility** — Report what works (projector, camera, Pi model) via the [hardware compat template](.github/ISSUE_TEMPLATE/hardware_compat.yml).
- **Code** — Fixes, new scenes, vision/tracking improvements, calibration UX, scripts.
- **Documentation** — Build guide improvements, troubleshooting, BOM updates.
- **Hardware** — Mount designs, wiring diagrams, BOM entries.

**Scope (in and out of scope)** is defined in the [README](README.md#scope). Design and scope decisions are discussed in issues or in [Architecture Decision Records (ADR)](docs/adr/README.md).

### Issue and PR labels

We use (or recommend) these labels for issues and PRs. Use them consistently so triage and filtering stay easy.

| Label | Use for |
|-------|--------|
| `bug` | Something is broken or incorrect. |
| `feature` | New capability or enhancement. |
| `docs` | Documentation-only changes. |
| `hardware` | Hardware compatibility, BOM, mounts, wiring. |
| `good first issue` | Small, well-scoped tasks suitable for first-time contributors. |

Maintainers: create a **good first issue** label and apply it to issues that are clearly scoped and documented (e.g. “Add a unit test for `reprojection_error`,” “Fix typo in 02_build_guide”). Point new contributors to [issues with that label](https://github.com/YOUR_ORG/rashbarrypi/labels/good%20first%20issue).

## Getting Started

### Running Locally

1. **Clone the repo**
   ```bash
   git clone https://github.com/YOUR_ORG/rashbarrypi.git
   cd rashbarrypi
   ```

2. **Install dependencies** (see [docs/02_build_guide.md](docs/02_build_guide.md) for full setup)
   ```bash
   make install
   ```
   Or manually: `pip install -r requirements.txt` (and `requirements-dev.txt` for development).

   **Reproducible install:** Run `make lock` to generate `requirements-lock.txt`. For reproducible installs (e.g. CI or matching a release), use `pip install -r requirements-lock.txt`. You may commit `requirements-lock.txt` so CI and contributors get the same dependency versions; see [00_best_practices](docs/00_best_practices.md) (lock file).

3. **Run tests**
   ```bash
   make test
   ```

4. **Run the app** (without Pi hardware, overlay/demo may be limited)
   ```bash
   make run
   ```

### Adding Sample Frames for Tests

To add sample frames or videos for offline/CI testing:

- Place images in `data/samples/frames/` and clips in `data/samples/videos/`.
- Keep files small (e.g. a few KB per frame) so the repo stays light.
- Document in a PR that the samples are for regression tests; avoid committing large binaries.

### Code Style

- **Python:** We use [Ruff](https://docs.astral.sh/ruff/) for linting and [Black](https://black.readthedocs.io/) for formatting.
  - Run `make lint` and `make format` before committing.
- **Docstrings:** Use Google or NumPy style for public modules, classes, and functions.
- **Types:** Use type hints where practical (mypy runs in CI).

### Pull Request Process

1. Open an issue or find an existing one that your PR addresses.
2. Create a branch from `main` (e.g. `fix/calibration-save`, `feat/particle-scene`).
3. Make your changes; ensure `make lint` and `make test` pass.
4. Open a PR using the [pull request template](.github/PULL_REQUEST_TEMPLATE.md).
5. Fill in the checklist (e.g. docs updated if needed, tests added).
6. A maintainer will review. We aim to triage PRs within a few days; response time may vary.

### Review process

- **What we check:** Tests pass (CI); code style (Ruff, Black); no unintended regressions; docs updated for user-facing or config changes; PR description and checklist match the change.
- **Typical timeline:** First review within about 1 week; follow-ups as needed. Timing depends on maintainer availability.
- You may be asked to make changes. Once approved, a maintainer will merge.

### First-time contributors

Look for issues labeled **good first issue**. Then: clone the repo, run `make install` and `make test`, pick one issue, make a small PR. We’ll guide you through review. For setup details, see [Getting started](#getting-started) above.

### Repository settings (maintainers)

- **Branch protection:** Enable on the default branch (e.g. `main`) with required status checks (CI) and, if desired, required pull request reviews. See GitHub → Settings → Branches.
- **Dependency graph:** Keep enabled (Settings → General) so Dependabot alerts and security updates work.

## Response Times

- **Issues:** We aim to triage (label, respond, or close) within **5 business days**.
- **PRs:** We aim to do a first review within **1 week**. Timing depends on maintainer availability.
- **Security:** See [SECURITY.md](SECURITY.md) for vulnerability reporting and response.

## Versioning and releases

- **Stable releases** use [Semantic Versioning](https://semver.org/) and git tags like `v1.2.3`. The [release workflow](.github/workflows/release.yml) runs on push to tags `v*`.
- **Pre-releases** use a hyphen and identifier, e.g. `v1.0.0-beta.1`, `v1.0.0-rc.2`. Do not move tags; cut a new tag for fixes.
- **When cutting a release:** Update the version in `pyproject.toml` (single source of truth). Also update `CITATION.cff` (`version` and `date-released`) and the “Latest stable” line in README.md so docs stay in sync.

## Questions

- For general questions, open a [Discussion](https://github.com/YOUR_ORG/rashbarrypi/discussions) (if enabled in the repo) or an issue. Discussions are optional; maintainers can enable them under Settings → General.
- For bugs and features, use the issue templates so we have the context we need.

Thanks for contributing.
