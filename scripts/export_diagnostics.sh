#!/usr/bin/env bash
# Bundle system info and config for bug reports (excludes calibration and secrets).
set -e
cd "$(dirname "$0")/.."
OUTPUT="${1:-diagnostics_bundle.tar.gz}"
exec python3 -m smartpi.cli export-diagnostics -o "$OUTPUT"
