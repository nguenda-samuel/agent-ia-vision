## 2026-10-12 - Icon-only buttons accessibility in CustomTkinter
**Learning:** Icon-only buttons (like 📸 and 🚀) lack textual context for screen readers and keyboard/mouse users. Standard Tkinter Toplevel tooltips anchored to the widget root position provide accessible hover hints and key shortcut guidance without adding external UI dependencies.
**Action:** Always attach CTkToolTip with functional description and shortcut hint (e.g. F9, Entrée) to icon-only buttons in CustomTkinter/Tkinter interfaces.
