## 2025-05-18 - Exposed Exception Details in User Interface
**Vulnerability:** Raw exception strings (`str(e)`) were appended directly into user-facing chat bubbles in `main_vision.py`.
**Learning:** Returning unhandled exception strings directly to the UI can expose sensitive internal details like API keys, internal URLs, or system paths.
**Prevention:** Always log detailed error messages internally while presenting generic, non-leaking user-friendly messages in user-facing components.
