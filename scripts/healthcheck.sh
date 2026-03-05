#!/usr/bin/env bash
# Smart Pi healthcheck — display, camera, FPS, CPU temp. Exit 0 = PASS.
set -e
cd "$(dirname "$0")/.."
echo "=== Display ==="
if command -v xdpyinfo &>/dev/null; then
  xdpyinfo -display :0 2>/dev/null | grep dimensions || true
else
  echo "xdpyinfo not installed; skip display check."
fi
echo "=== Camera + FPS (Python) ==="
python3 -m smartpi.cli healthcheck
echo "=== Done ==="
