"""Benchmark detector FPS on sample frames. Run with: python -m benchmarks.bench_detector."""

from __future__ import annotations

import time
from pathlib import Path

# Optional: add sample frame path and run detect_bright/detect_ir in a loop, report FPS.
def main() -> None:
    frames_dir = Path(__file__).parent.parent / "data" / "samples" / "frames"
    if not frames_dir.exists() or not list(frames_dir.glob("*.png")):
        print("No sample frames in data/samples/frames/. Add some for benchmarking.")
        return
    # Placeholder: real benchmark would load frames and time detect_* calls.
    print("Benchmark placeholder: add frame iteration and timing.")

if __name__ == "__main__":
    main()
