## 2026-09-25 - CustomTkinter Icon Button Tooltips & Focus Events
**Learning:** CustomTkinter buttons composite inner widgets (`_canvas`), so accessibility tooltips must bind both `<Enter>`/`<Leave>` for mouse hover and `<FocusIn>`/`<FocusOut>` on the parent widget and `_canvas` for keyboard tab navigation.
**Action:** When adding tooltips to CustomTkinter components, always bind focus events to both the widget wrapper and its inner canvas.
