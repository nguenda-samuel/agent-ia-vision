## 2026-10-07 - Downscaling Haar Cascade face detection in PrivacyFilter

**Learning:** Running OpenCV `CascadeClassifier.detectMultiScale` on raw full-resolution screen frames (768x768 / 1080p) introduces significant CPU latency (~170ms per frame). Downscaling the grayscale frame by 0.5x reduces face detection latency to ~50ms (~3.4x speedup) while maintaining detection sensitivity when `minSize` is adjusted proportionally. Additionally, working directly in RGB format avoids redundant RGB<->BGR conversion overhead (~10ms per frame).

**Action:** Downscale large screen frame copies before CPU-heavy vision routines like OpenCV cascades, and scale bounding box coordinates back to full resolution for pixel manipulation.
