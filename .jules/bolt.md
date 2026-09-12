## 2026-03-30 - Downscaling Gray Images Before Haar Cascade Detection
**Learning:** Running `CascadeClassifier.detectMultiScale` directly on high-resolution (1080p+) screenshots causes a significant bottleneck (~635ms) during screen redaction in `PrivacyFilter`. Downscaling the grayscale frame by 50% (`fx=0.5, fy=0.5`) before face detection and rescaling coordinates back reduces multi-scale search overhead by 3x (~210ms per frame).
**Action:** Always downscale high-res grayscale frames before running OpenCV Haar Cascade face detection.
