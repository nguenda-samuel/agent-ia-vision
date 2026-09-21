## 2026-09-21 - CustomTkinter Icon-Only Button Accessibility
**Learning:** CustomTkinter icon-only buttons (`📸`, `🚀`) lack visual hints and accessible tooltips out of the box, confusing mouse and keyboard users.
**Action:** Bind `<Enter>`, `<Leave>`, `<FocusIn>`, and `<FocusOut>` events to show non-intrusive `Toplevel` tooltips for icon-only buttons without adding third-party dependencies.
