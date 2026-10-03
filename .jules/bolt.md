## 2026-10-03 - OpenCV Face Detection & Color Conversion Overhead in Vision Assistant

**Learning:** OpenCV Haar Cascade `detectMultiScale` on full-resolution screenshots (e.g. 1080p / 768p) evaluates thousands of multi-scale sliding windows, causing substantial per-frame latency (~900ms on 1080p). Additionally, round-trip RGB <-> BGR color conversions before and after array operations allocate full-resolution frame arrays unnecessarily. Downscaling grayscale images to max dimension 400 before cascade classification and operating directly on RGB NumPy arrays reduced `PrivacyFilter` latency by 60% on 768p frames (~267ms -> ~112ms) and by 82% on 1080p frames (~912ms -> ~163ms).

**Action:** For vision pipeline pre-processing, always downscale grayscale images before running feature/object detectors like Haar cascades or HOG, and avoid redundant color space conversions when NumPy slice operations support RGB directly.
