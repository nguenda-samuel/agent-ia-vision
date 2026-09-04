## 2026-09-04 - Direct RGB Image Processing in OpenCV Redaction

**Learning:** OpenCV functions like `cv2.cvtColor(..., cv2.COLOR_RGB2GRAY)` and `cv2.GaussianBlur(...)` operate directly on RGB numpy arrays. Converting RGB arrays to BGR and back to RGB before/after redaction introduces redundant full-resolution array allocations and memory copies.

**Action:** When working with PIL images converted to numpy arrays, convert directly to GRAY for feature/contour detection and perform array slice updates (such as blurring) on the original RGB numpy array.
