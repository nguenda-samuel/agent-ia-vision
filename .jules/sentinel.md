## 2026-03-29 - Sanitizing Unhandled Exceptions in Tkinter Chat UI
**Vulnerability:** Raw exception strings (`err_msg`) were rendered directly into the user chat UI bubbles in `main_vision.py` upon unexpected execution failures.
**Learning:** Displaying `str(e)` directly in desktop agent UI chat bubbles leaks internal system paths, configuration details, or API error responses to the UI layer (CWE-209).
**Prevention:** Always log detailed exception messages internally via console logging while presenting generic, user-safe error messages in the user interface.
