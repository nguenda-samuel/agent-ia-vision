## 2025-10-23 - OpenCV GaussianBlur ROI Sizing in Privacy Redaction
**Vulnerability:** Privacy redaction in OpenCV threw an assertion error (`ksize.width <= src.cols`) when redacting input boxes with height smaller than the fixed kernel size (e.g., 25px height vs 51px kernel), crashing screen filtering or bypassing redaction. Non-RGB image formats (RGBA) also raised `cv2.cvtColor` errors.
**Learning:** Hardcoded OpenCV kernel sizes assume minimum ROI dimensions. When dynamic contour detection yields smaller bounding boxes or different color modes, unhandled OpenCV exceptions break the privacy pipeline.
**Prevention:** Always convert PIL screenshots to standard RGB before CV processing and dynamically constrain filter kernel sizes based on ROI dimensions (`min(dim, max_ksize)`).
