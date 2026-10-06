## 2026-10-06 - Downscaling Image for OpenCV Feature Detection

**Learning:** Running OpenCV Haar Cascade face detection (`cv2.CascadeClassifier.detectMultiScale`) and contour thresholding directly on full 1080p/4K resolution desktop screenshots is bottlenecked by $O(N)$ pixel processing. Downscaling the grayscale matrix by 50% (`scale=0.5`) before detection reduces total pixel count by 75% and improves detection execution time by ~7x (from ~710ms down to ~100ms) with minimal impact on detection accuracy.
**Action:** When performing computer vision feature detection (face cascades, contour finding, etc.) on high-resolution screenshots before ROI extraction, downscale the image for detection and scale coordinates back up when applying full-resolution ROI transformations.
