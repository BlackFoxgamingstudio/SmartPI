# Performance notes

- **Target FPS:** ≥ 20 FPS for pointer tracking (prefer ≥ 30).
- **Detection:** Lower resolution (e.g. 320x240) improves FPS; tune threshold and blur per profile.
- **Calibration:** Homography solve is one-time; apply_homography is cheap per frame.
- Run `bench_detector.py` with sample frames to measure detector throughput.
