# Palette's Journal - Critical UX & Accessibility Learnings

## 2025-05-18 - Tooltips for Icon-Only Buttons in CustomTkinter
**Learning:** Icon-only buttons (like `📸` and `🚀`) in CustomTkinter desktop applications lack native ARIA labels or default hover descriptions, making them inaccessible and ambiguous for screen readers and new users alike. Adding a lightweight Tkinter `Toplevel` tooltip on `<Enter>`/`<Leave>` events provides clear context and shortcut hints (e.g. F9, Enter).
**Action:** Always wrap icon-only buttons with a `ToolTip` component in CustomTkinter/Tkinter desktop applications.
