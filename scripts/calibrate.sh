#!/usr/bin/env bash
# Run calibration wizard. Delegates to: smartpi calibrate
set -e
exec python3 -m smartpi.cli calibrate "$@"
