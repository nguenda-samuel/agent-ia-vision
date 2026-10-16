## 2026-09-04 - Eliminate redundant frame color conversions in PrivacyFilter

**Learning:** Converting high-resolution PIL RGB screen capture frames to BGR via `cv2.cvtColor(img, cv2.COLOR_RGB2BGR)` before grayscale processing and then back to RGB with `cv2.COLOR_BGR2RGB` allocates two full-frame array copies and performs millions of unnecessary byte ops per call. OpenCV functions such as `cv2.COLOR_RGB2GRAY` and channel-independent operations like `cv2.GaussianBlur` work directly on RGB array slices in place.

**Action:** Convert RGB images directly to grayscale with `cv2.COLOR_RGB2GRAY` and apply in-place OpenCV blurs directly on RGB array slices, avoiding redundant BGR conversions.
