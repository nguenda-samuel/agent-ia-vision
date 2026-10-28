## 2026-03-23 - CustomTkinter Async Button State Management
**Learning:** When executing background async operations in CustomTkinter / Tkinter GUI applications, interactive submit buttons should be visually disabled (`state="disabled"`) during processing and re-enabled in the `finally:` block or main thread callback to give clear interaction feedback and prevent duplicate triggers.
**Action:** Always wrap async processing triggers with UI input state toggles and ensure re-enabling in `finally:` blocks or `app.after(0, ...)` callbacks.
