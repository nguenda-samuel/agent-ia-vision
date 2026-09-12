## 2026-09-12 - Parameterized SQLite Caching and OpenCV Version Compatibility
**Vulnerability:** Potential SQL injection vulnerability when caching AI query responses and broken privacy filtering due to OpenCV version incompatibility.
**Learning:** `ai_engine.py` relied on a `database` caching module to retrieve and store text intent query responses. Using unparameterized queries or string concatenation in database operations exposes SQLite to SQL injection. Additionally, `opencv-python==5.x` breaks `cv2.CascadeClassifier`, failing the privacy face-redaction filter.
**Prevention:** Always use parameterized SQL queries (`?`) in database functions to sanitize input, and pin `opencv-python==4.10.0.84` to keep privacy redactions functional.
