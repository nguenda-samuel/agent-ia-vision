# Palette's UX Journal

## 2026-09-09 - Accessible Tooltips for Icon-Only CustomTkinter Buttons
**Learning:** CustomTkinter icon-only buttons (like `📸` or `🚀`) lack built-in screen reader descriptions and textual hints. CustomTkinter widgets support Tkinter event bindings (`<Enter>`, `<Leave>`, `<FocusIn>`, `<FocusOut>`), allowing a lightweight `CTkToolTip` popup to show actionable text and shortcut key hints (e.g., F9, Return) on both mouse hover and keyboard focus.
**Action:** Always wrap icon-only CTkButton components with `CTkToolTip` to clarify their purpose and display keyboard shortcuts for accessibility.
