## 2025-05-18 - [Preventing OpenCV GaussianBlur Assertion Crashes on Empty ROIs]
**Vulnerability:** Slicing regions of interest (ROI) from images in `PrivacyFilter` could produce empty arrays when coordinates fall outside or on invalid boundaries, causing `cv2.GaussianBlur` to raise an OpenCV assertion error (`!_src.empty()`) and crash the privacy filtering pipeline.
**Learning:** OpenCV functions do not fail silently on zero-size numpy slices; unhandled assertion crashes in security/privacy filters can cause denial of service or result in unblurred sensitive data being exposed downstream.
**Prevention:** Always validate that bounding rectangle dimensions and ROI array sizes are non-zero (`roi.size > 0`) before executing OpenCV matrix transformations or blurs.
