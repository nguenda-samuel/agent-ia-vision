## 2026-10-22 - Non-RGB PIL image modes bypass or crash PrivacyFilter redaction
**Vulnerability:** Non-RGB PIL image modes (such as RGBA, L, or P) cause `cv2.cvtColor` channel format mismatch errors during privacy redaction processing in `PrivacyFilter.redact_sensitive_data`.
**Learning:** In applications taking arbitrary screen captures or PIL images, image color channels and modes can vary (e.g. RGBA screenshots from MSS/macOS/Linux). OpenCV operations expecting 3-channel BGR/RGB will fail if images are not explicitly converted to RGB mode first.
**Prevention:** Always convert PIL images to RGB mode (`pil_image.convert("RGB")`) before passing to OpenCV image processing pipelines.
