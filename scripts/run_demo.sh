#!/usr/bin/env bash
# Run the demo. Delegates to: smartpi run (optionally --fullscreen)
set -e
exec python3 -m smartpi.cli run "$@"
