#!/usr/bin/env bash
# Install dependencies and optional systemd service on Raspberry Pi.
# See docs/02_build_guide.md for full instructions.
set -e
echo "Installing Smart Pi dependencies..."
pip install -r requirements.txt
echo "Optional: copy src/smartpi/services/systemd/smartpi.service to /etc/systemd/system/ and enable."
exit 0
