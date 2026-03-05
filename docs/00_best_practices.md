# 100+ Open Source Best Practices for a Fully Documented, Coded Repo

A checklist of research-backed best practices for a fully documented, fully coded GitHub open source project. Use this to keep the project aligned with high standards. Grounded in GitHub Docs, Open Source Guides, CITATION.cff, hardware/BOM practices, and CI/CD/documentation standards.

**Total: 152 practices** across 11 categories. Treat as a checklist; adopt what fits your project size and goals.

---

## 1. Repository structure and essential files (18)

1. Include a clear **README.md** at repo root (GitHub surfaces it automatically).
2. Use a **LICENSE** file with an OSI-approved license (e.g. MIT, Apache 2.0, GPL).
3. Add **CODE_OF_CONDUCT.md** (e.g. Contributor Covenant) and link it from README.
4. Add **CONTRIBUTING.md** with types of contributions, setup, and style expectations.
5. Add **SECURITY.md** for vulnerability disclosure and security policy.
6. Add **CHANGELOG.md** (or link to it) for release history.
7. Add **CITATION.cff** for software citation (authors, version, title, DOI/repo; GitHub shows "Cite this repository").
8. Add **.gitignore** appropriate to language and tooling (e.g. Python, Node, build artifacts).
9. Add **.editorconfig** for consistent indentation, line endings, and charset across editors.
10. Use a **lock file** (e.g. `uv.lock`, `poetry.lock`, `package-lock.json`) for reproducible installs. *This project: optional `make lock` → `requirements-lock.txt`; see [CONTRIBUTING](../CONTRIBUTING.md).*
11. Keep **dependency list** in one place (e.g. `pyproject.toml`, `requirements.txt`, `package.json`).
12. Add **ROADMAP.md** (or equivalent) for public roadmap and phases (e.g. v0.1–v1.0).
13. Use **Makefile** (or equivalent) for common commands (install, test, lint, run).
14. Put **issue templates** under `.github/ISSUE_TEMPLATE/` (e.g. bug_report.yml, feature_request.yml).
15. Add **pull request template** (e.g. `.github/PULL_REQUEST_TEMPLATE.md`).
16. Add **CODEOWNERS** (e.g. `.github/CODEOWNERS`) for review ownership and governance.
17. Prefer **branch protection** and required status checks on default branch.
18. Keep **config and secrets** out of repo (env files in .gitignore; use env vars or secret managers).

---

## 2. README and top-level documentation (16)

19. README states **who maintains** the project and how to get help.
20. README explains **why the project exists** and what problem it solves.
21. README describes **what the project does** (features, scope).
22. README provides **how to get started** (install, minimal run, link to full guide).
23. Include **badges** (build status, coverage, license) where useful and accurate.
24. Add **Table of Contents** for long READMEs.
25. Document **requirements** (OS, hardware, runtime, optional components).
26. Link to **detailed docs** (e.g. `docs/02_build_guide.md`) from README.
27. Mention **known issues / limitations** and where to report (e.g. GitHub Issues).
28. Link to **CHANGELOG** and **CONTRIBUTING** from README.
29. Use **plain language** and define jargon on first use.
30. Keep **most important info** near the top; structure with clear headings.
31. Use **consistent formatting** (headings, lists, code blocks).
32. Include **one or two code/usage snippets** for quick validation.
33. For hardware: link to **BOM** and **build guide** from README.
34. State **support level** (e.g. community, best-effort) and response expectations.

---

## 3. Documentation (docs/) (18)

35. Provide an **overview** (e.g. `00_overview.md`) that orients new readers.
36. For hardware: maintain **bill of materials** (BOM) with part numbers, quantities, and optional **bom.csv**.
37. Write a **step-by-step build guide** (e.g. `02_build_guide.md`) so a stranger can replicate.
38. Document **system architecture** (e.g. `04_system_architecture.md`) and data/control flow.
39. Document **calibration / setup UX** (e.g. `05_calibration_ux.md`) with screenshots or diagrams.
40. Maintain **troubleshooting** (e.g. `07_troubleshooting.md`) for common failures (no camera, low FPS, alignment).
41. Document **safety and power** (e.g. `08_safety_and_power.md`) where relevant.
42. Include **accessibility and inclusion** (e.g. `09_accessibility_and_inclusion.md`) in docs and design.
43. Use **Mermaid or similar** for architecture/flow diagrams (e.g. `diagrams/architecture.mmd`) and keep sources in repo.
44. Store **images/diagrams** under `docs/images/` or `docs/diagrams/` and reference from markdown.
45. Provide **operator/demo** docs (e.g. showcase script, operator checklist) for reproducible demos.
46. Document **repair and maintenance** (e.g. repair-forward notes, surplus sourcing) for longevity.
47. Keep docs **concise**: only what's needed for the majority of users.
48. **Version and date** key docs (e.g. "Last updated: YYYY-MM-DD") where it helps.
49. Cross-link between docs (e.g. "See 02_build_guide.md for setup").
50. Prefer **one concept per section**; use headings and lists for scanability.
51. For APIs: document **parameters, return values, and errors** (or link to auto-generated API docs).
52. Document **config options** (e.g. `configs/app.yaml`, `configs/profiles/*.yaml`) with purpose and defaults.

---

## 4. Code quality and in-repo logic (18)

53. Use a **single, consistent language/style** per module (e.g. Python style guide or Black/Ruff).
54. **Docstrings** for public modules, classes, and functions (Google or NumPy style where applicable).
55. **Type hints** (or equivalent) where the language supports them (e.g. Python, TypeScript).
56. **No commented-out dead code** in main branches; remove or ticket and remove later.
57. **Meaningful names** for variables, functions, and files; avoid single-letter names except in narrow scope.
58. **Small, testable functions**; separate I/O and side effects from pure logic where possible.
59. **Single responsibility** per module/class; clear separation (e.g. capture vs detect vs calibrate vs render).
60. **Config over hardcoding**: paths, URLs, thresholds in config files or env, not in code.
61. **Explicit dependencies**: inject or pass dependencies (e.g. camera, config) for testability.
62. **Structured logging** (levels, context) instead of print for production paths.
63. **Error handling**: catch specific exceptions; fail fast with clear messages or logs.
64. **No secrets in code**; use env vars or secret managers and document required env in README/docs.
65. **EditorConfig** respected: indentation, line endings, charset consistent (enforced by tooling if possible).
66. **Linting** (e.g. Ruff, ESLint) in CI; fix or explicitly ignore with justification.
67. **Formatting** (e.g. Black, Prettier) automated so diffs stay clean.
68. **Unused imports and dead code** removed; linters/CI can enforce.
69. **Public API surface** documented (docstrings + high-level overview in docs).
70. **Magic numbers** replaced by named constants or config; document units and rationale.

---

## 5. Testing and CI/CD (18)

71. **Unit tests** for core logic (e.g. calibration math, tracking, config loading) so CI can run without hardware.
72. **Sample data** (e.g. `data/samples/frames/`, `data/samples/videos/`) for offline/regression tests.
73. **CI workflow** (e.g. `.github/workflows/ci.yml`) runs on push/PR: lint, format, unit tests, type check.
74. **No flaky tests**: tests deterministic or clearly marked as integration/slow; fix or quarantine flaky tests.
75. **Test naming** that describes behavior (e.g. `test_calibration_rejects_insufficient_points`).
76. **Fast feedback**: keep default CI under a few minutes; optional nightly or hardware jobs separately.
77. **Fail CI on lint/format** so main branch stays clean.
78. **Coverage reporting** (optional but recommended) for critical paths; avoid gaming with useless tests.
79. **Type checking** in CI (e.g. mypy, TypeScript strict) where adopted.
80. **Separate workflows** for release (e.g. `release.yml`) and docs (e.g. `docs.yml`) if needed.
81. **Reproducible test env**: same Python/Node version in CI as in README; use lock files.
82. **No external service calls** in unit tests by default; mock or use fixtures.
83. **Clear failure messages** and logs so contributors can fix without deep debugging.
84. **Branch protection**: require passing CI (and optional review) before merge.
85. **Dependency caching** in CI (e.g. pip cache, npm cache) to speed runs.
86. **Matrix builds** only if you need multiple versions/OS; keep minimal for maintainability.
87. **Artifacts** (e.g. built docs, binaries) published only from tagged release or explicit workflow.
88. **Security scanning** in CI: dependency audit, secret scanning, and optional SAST where applicable.

---

## 6. Community, contribution, and governance (16)

89. **CONTRIBUTING.md** explains: types of contributions, how to run locally, how to add samples, code style, and PR process.
90. **Code of Conduct** linked from README and CONTRIBUTING; enforce consistently.
91. **Issue templates** (bug, feature, hardware compat) guide reporters to provide enough context.
92. **PR template** asks for: related issue, description, testing done, and checklist (e.g. docs updated).
93. **Labels** for issues/PRs (e.g. bug, feature, docs, good first issue, hardware) and use them consistently.
94. **Response expectations** documented (e.g. "we aim to triage within N days"); keep communication public.
95. **Review process** documented: who reviews, what is checked, and how long to expect.
96. **CODEOWNERS** so relevant maintainers are requested for reviews automatically.
97. **MAINTAINERS.md** (optional) with names and contact for larger projects.
98. **First-time contributor** guidance: label "good first issue," document setup, and point to small tasks.
99. **Changelog/credit** contributors in release notes or CONTRIBUTORS file where appropriate.
100. **No private decisions** on design/scope that affect contributors; discuss in issues or ADRs.
101. **Project vision and goals** written down (e.g. in README or ROADMAP) so priorities are clear.
102. **Explicit scope**: what's in scope and out of scope (e.g. "we don't support Windows").
103. **Time/availability** of maintainers stated if relevant (e.g. "maintained in spare time").
104. **Single source of truth**: avoid duplicating contribution rules in many places; link from README/CONTRIBUTING.

---

## 7. Security and dependencies (12)

105. **SECURITY.md** with: how to report vulnerabilities, expected response time, and disclosure policy.
106. **Dependabot** (or similar) enabled: security updates and version updates; use `dependabot.yml` to tune.
107. **Dependency graph** enabled on GitHub so alerts and Dependabot work.
108. **No committed secrets**; use secret scanning and pre-commit/CI checks.
109. **Minimal dependencies**: only add deps that are needed; prefer std lib or well-maintained packages.
110. **Pin critical versions** (or use lock file) so builds are reproducible and upgrades are intentional.
111. **Review Dependabot/renovate PRs** promptly; automate merge for patch-only where policy allows.
112. **Vulnerability alerts** addressed with a documented process (triage, fix, release, disclose).
113. **Supply chain**: prefer official or widely used sources; verify hashes where practical.
114. **Principle of least privilege** in scripts and deployment (e.g. avoid root where not needed).
115. **Secure defaults** in config (e.g. no debug endpoints on by default in production).
116. **License compliance**: track licenses of dependencies; document in NOTICE or docs if required.

---

## 8. Release and versioning (10)

117. **Semantic versioning** (MAJOR.MINOR.PATCH) for public API and releases.
118. **Changelog** updated with each release (e.g. Conventional Changelog or manual "What's new").
119. **Git tags** for releases (e.g. `v1.0.0`); use consistent tag format.
120. **Release notes** (e.g. GitHub Releases) with summary, highlights, and upgrade notes.
121. **Breaking changes** called out clearly in changelog and release notes; bump MAJOR.
122. **Stable version** clearly indicated (e.g. "latest stable: v1.0" in README).
123. **Pre-release** tags (e.g. `v1.0.0-beta.1`) for unstable releases.
124. **One release per tag**; avoid moving tags; prefer new patch for fixes.
125. **CITATION.cff** version field updated (or automated) to match release tag.
126. **Artifacts** (binaries, docs, BOM) attached to GitHub Release where useful.

---

## 9. Hardware and reproducibility (12)

127. **BOM** with part numbers, quantities, and preferred/verified suppliers (e.g. `hardware/bom.csv`).
128. **Build guide** that leads to "demo running" without in-person help.
129. **Calibration** documented (steps, validation, troubleshooting) so operators can recalibrate.
130. **Config profiles** (e.g. classroom, dark room, daylight) for different environments.
131. **Hardware compat** issue template (e.g. projector/camera/OS) to collect compatibility data.
132. **Design files** (e.g. STL, CAD) under version control with README (e.g. `hardware/camera_mount/`).
133. **Wiring/schematics** (e.g. `ir_pen/wiring_diagram.svg`) and assembly notes.
134. **Docker/dev container** (e.g. `docker/Dockerfile.dev`) for x86 dev without Pi hardware.
135. **Scripts** for install, kiosk, calibration, run, healthcheck, diagnostics (e.g. `scripts/install_pi.sh`).
136. **Healthcheck** script that validates display, camera, FPS, and permissions.
137. **Diagnostics export** (e.g. `export_diagnostics.sh`) for bug reports without leaking secrets.
138. **Reproducible builds**: lock file for deps; Docker base image by digest if you ship images.

---

## 10. Accessibility and inclusion (8)

139. **Accessibility** considered in UI (contrast, focus, keyboard/single-pointer where applicable).
140. **Docs** readable by screen readers (headings, lists, alt text for images).
141. **Inclusive language** in docs and UI (e.g. avoid assumptions about ability or background).
142. **Inclusive Design Guide** or similar principles referenced where relevant.
143. **Feedback channels** open to all (e.g. issues, discussions) and Code of Conduct enforced.
144. **Document** known accessibility limitations and workarounds.
145. **Default font size and contrast** meet minimum guidelines (e.g. WCAG) where applicable.
146. **Calibration/demo** operable with minimal fine motor control (e.g. big targets, few steps).

---

## 11. Miscellaneous (6)

147. **.gitignore** includes IDE, OS, and build artifacts (e.g. `__pycache__`, `.env`, `dist/`).
148. **Changelog** format consistent (e.g. "Added," "Fixed," "Changed") and linkable.
149. **Stale bot** (optional) to close inactive issues with a comment and label.
150. **Discussions** (optional) for Q&A and ideas without overloading issues.
151. **Document** port numbers and URLs (e.g. 3036 frontend, 3005 backend) in one place.
152. **Single source of truth** for version (e.g. `pyproject.toml` or `package.json`); derive elsewhere.

---

## Suggested next steps

1. **Tick off** items already done (e.g. README, LICENSE, docs layout) and mark "N/A" where not applicable.
2. **Prioritize** gaps (e.g. CITATION.cff, SECURITY.md, CODEOWNERS, Dependabot) by impact and effort.
3. **Revisit** this list when adding new workstreams or preparing for a major release.

See also: [build.md](../build.md) for repo structure and workstreams aligned with these practices.
