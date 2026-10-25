## 2025-05-18 - Tooltip and Keyboard Focus Accessibility in CustomTkinter
**Learning:** CustomTkinter icon-only buttons lack inherent ARIA labels or standard screen reader text in Tkinter/X11 environments. Binding custom tooltips (`CTkToolTip`) to both `<Enter>/<Leave>` (hover) and `<FocusIn>/<FocusOut>` (keyboard navigation) guarantees visible feedback and descriptive context for keyboard and pointer users alike.
**Action:** Always wrap icon-only or visual symbol buttons in `CTkToolTip` attached to mouse and focus events, and include explicit text alongside icons where possible.
