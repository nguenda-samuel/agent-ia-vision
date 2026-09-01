## 2026-09-01 - CustomTkinter Keyboard Shortcuts & Window Focus
**Learning:** In CustomTkinter apps with hidden or top-level windows, binding `<Escape>` to withdraw/hide windows and explicitly focusing the main entry widget on show significantly improves keyboard accessibility and usability without altering existing layouts.
**Action:** Always ensure modal or top-level dialogs/windows can be dismissed with `Escape` and that entry fields receive focus when shown.
