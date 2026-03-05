# Maintainers

This project is maintained by the Smart Pi community.

## How to get in touch

- **Issues and PRs:** Use [GitHub Issues](https://github.com/YOUR_ORG/rashbarrypi/issues) and [Pull Requests](https://github.com/YOUR_ORG/rashbarrypi/pulls).
- **Security:** See [SECURITY.md](SECURITY.md) for vulnerability reporting.
- **Contributing:** See [CONTRIBUTING.md](CONTRIBUTING.md) for how to contribute.

## Response expectations

We aim to triage issues within a few business days and to do a first review on PRs within about a week. The project may be maintained in spare time; response times can vary. We keep communication public where possible.

## Maintainer checklist (before or after publishing)

- **Branch protection:** Default branch (e.g. `main`) — require CI and optionally required reviews (see CONTRIBUTING).
- **Dependency graph:** Keep enabled for Dependabot and security alerts.
- **Stale workflow:** To enable weekly stale-issue automation, uncomment the `schedule` in [.github/workflows/stale.yml](.github/workflows/stale.yml); otherwise it runs only via **Actions → Stale → Run workflow**.
- **Placeholders:** Replace `YOUR_ORG` and `YOUR_GITHUB_USERNAME` in README, CONTRIBUTING, CODEOWNERS, and CITATION.cff.
