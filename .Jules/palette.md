# Palette's Journal - Critical Learnings

## 2025-09-02 - CustomTkinter Button State Feedback for Async Operations
**Learning:** In Tkinter/CustomTkinter desktop applications, submitting an async task (like vision analysis) leaves action buttons clickable unless explicitly disabled during processing, which can confuse users and lead to redundant background tasks. Thread safety requires updating UI element states on the main GUI thread (`after(0, ...)`).
**Action:** Always disable action buttons when triggering async requests and safely restore them via `after(0, ...)` in `finally` blocks or stop handlers.
