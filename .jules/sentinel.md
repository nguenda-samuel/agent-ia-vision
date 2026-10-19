## 2025-05-10 - Sensitive Error Redaction and Input Validation in Gemini Vision Agent
**Vulnerability:** Unsanitized API error responses could leak secret Gemini API keys (`key=...`, `AIzaSy...`) in exception strings logged to stdout or rendered in the user chat interface. Oversized `user_intent` strings could also cause prompt bloat/DoS issues.
**Learning:** Exception messages from third-party client SDKs (like `google-genai`) may embed full request URLs containing API key query parameters.
**Prevention:** Always scrub known secret patterns (e.g. `AIzaSy...` and `key=...` query parameters) from error messages before printing or returning them in user UI / logs, and sanitize/truncate input strings at boundaries.
