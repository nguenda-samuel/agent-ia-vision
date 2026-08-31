# Palette's Journal - CustomTkinter & Desktop UX Learnings

## 2026-08-30 - CustomTkinter Icon-Only Tooltips & Escape Binding
**Learning:** Icon-only buttons (`📸`, `🚀`) in CustomTkinter lack accessible label attributes. Adding a lightweight `CTkToolTip` helper using `<Enter>`/`<Leave>` hover bindings with `add="+"` preserves existing click handlers while giving immediate visual context and shortcut hints (`F9`, `Entrée`). Binding `<Escape>` at both widget and top-level window level allows consistent keyboard dismissal.
**Action:** Use `CTkToolTip` for all icon-only buttons and ensure `<Escape>` bindings match across secondary and main windows.
