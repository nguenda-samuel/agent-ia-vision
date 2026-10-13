## 2025-02-23 - Downscaling input frames for OpenCV Haar Cascade Detection

**Learning:** `cv2.CascadeClassifier.detectMultiScale` sliding window analysis cost grows quadratically with input image size. For 1080p desktop screenshots, detecting faces on full-resolution frames took ~640ms per frame. Downscaling the grayscale image by 50% prior to running face detection reduced execution time to ~200ms while preserving face detection quality (scaling coordinates back by 2x). Additionally, avoiding unnecessary `RGB -> BGR -> GRAY -> BGR -> RGB` roundtrip color conversions shaved off extra latency and memory churn.

**Action:** When performing cascade object detection or feature extraction on full-resolution screenshots, downscale the grayscale input image first, and scale back bounding box coordinates. Always convert directly from source color space (RGB) to GRAY without passing through intermediate spaces (BGR).
