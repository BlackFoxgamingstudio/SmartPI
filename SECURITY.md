# Security Policy

## Supported Versions

We release patches for security vulnerabilities for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |
| < 0.1   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it responsibly.

**How to report:**

1. **Do not** open a public GitHub issue for security vulnerabilities.
2. Email the maintainers (see [MAINTAINERS.md](MAINTAINERS.md) if present) or open a **private** security advisory on GitHub: Repository → Security → Advisories → New draft security advisory.
3. Include a clear description, steps to reproduce, and impact if possible.

**What to expect:**

- We aim to acknowledge your report within **5 business days**.
- We will work on a fix and keep you updated. We may ask for clarification.
- Once a fix is ready, we will release a patch and credit you in the release notes (unless you prefer to remain anonymous).
- We follow **coordinated disclosure**: we will not disclose the vulnerability publicly before a fix is available, and we ask reporters to do the same.

**Target response times by severity:**

| Severity | Description | Target (fix or mitigation) |
|----------|-------------|----------------------------|
| Critical | Remote code execution, auth bypass, data exposure | 14 days |
| High     | Significant impact; hard to exploit | 30 days |
| Low      | Limited impact or easy to work around | Next release |

## Disclosure Policy

- Security fixes are released as patch versions (e.g. 0.1.1).
- After a fix is released, we may publish a brief advisory describing the issue and the fix.
- We do not disclose unfixed vulnerabilities without agreement from the reporter.

Thank you for helping keep this project and its users safe.
