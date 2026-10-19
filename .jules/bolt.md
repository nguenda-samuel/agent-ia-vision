## 2025-10-19 - OpenCV Haar Cascade Face Detection Bottleneck

**Learning:** OpenCV's `detectMultiScale` on full-resolution screenshots (e.g. 768x768+) is a major bottleneck taking ~170ms per frame. Downscaling the grayscale image by 50% before running `detectMultiScale` (and downscaling `minSize` proportionally) speeds up detection by ~3.3x with minimal accuracy loss for typical face sizes, cutting total privacy redaction runtime by ~60% (~117ms per frame).
**Action:** Always downscale input grayscale images when running OpenCV Haar cascades for face detection in real-time frame processing pipelines.
