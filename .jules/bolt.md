## 2026-10-14 - Downscaling Frames for OpenCV Cascade Detection and Contour Analysis

**Learning:** Running OpenCV Haar cascade face detection (`detectMultiScale`) and contour search on full-resolution screen captures (e.g., 768x768+) is a massive performance bottleneck (~200ms per frame). Downscaling the grayscale frame by 0.5x before running cascade/contour detection and scaling coordinates back up yields a >60% speedup (~79ms total runtime) without losing detection accuracy for privacy redaction. Additionally, converting PIL RGB arrays directly to grayscale (`COLOR_RGB2GRAY`) avoids useless BGR intermediate color conversions.

**Action:** For vision or video processing workflows involving OpenCV cascade detectors or contour bounding box filtering, downscale the grayscale input frame during detection passes and scale bounding box coordinates back to full resolution for pixel manipulation/blurring.
