## 2025-05-18 - Tooltips for Icon-Only CustomTkinter Buttons
**Learning:** CustomTkinter icon-only buttons (like 📸 and 🚀) lack accessible descriptions for hover and screen readers. A lightweight `CTkToolTip` wrapper using `tk.Toplevel` on `<Enter>` and `<Leave>` events provides necessary UX context without modifying component geometry or styling.
**Action:** Always attach tooltips or accessible hover hints to icon-only buttons in Tkinter/CustomTkinter desktop applications.
