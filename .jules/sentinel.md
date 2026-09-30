# Sentinel's Journal

## 2026-09-30 - Reversible Blur Security Flaw in Privacy Redaction
**Vulnerability:** `PrivacyFilter` used `cv2.GaussianBlur` on sensitive screen areas (detected faces and password input fields). Gaussian blur is mathematically reversible and does not securely redact sensitive user credentials or visual PII before transmitting screenshots to external cloud APIs.
**Learning:** For privacy and security redactions, image blurring or pixelation must be avoided in favor of complete, irreversible solid-color overlay masking (`cv2.rectangle` with thickness -1).
**Prevention:** Always use solid opaque masking (`cv2.rectangle(..., fill=-1)`) for redacting PII or credentials in image processing filters. Also ensure SQL query operations use parameter binding (`?`) in database helper modules.
