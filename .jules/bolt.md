## 2026-09-02 - Redundant OpenCV Color Conversions on PIL Images
**Learning:** OpenCV functions like `GaussianBlur` work directly on 3-channel numpy arrays regardless of channel order (RGB vs BGR). Converting PIL image arrays from RGB to BGR and back to RGB allocates large intermediate arrays (e.g. ~6MB per 1080p frame) and adds ~23ms of overhead per screenshot.
**Action:** Keep PIL-derived numpy arrays in native RGB channel order and convert directly to grayscale with `cv2.COLOR_RGB2GRAY` when grayscale is needed for computer vision algorithms (face detection, contour extraction).
