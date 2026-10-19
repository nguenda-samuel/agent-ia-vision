## 2025-05-18 - Tooltips for CustomTkinter Icon-Only Buttons
**Learning:** CustomTkinter icon buttons (`CTkButton` with emoji/icons only) lack built-in accessibility/tooltip text, leaving desktop users unsure of their actions without text labels or hover tooltips.
**Action:** Use a lightweight Tkinter `Toplevel` overlay bound to `<Enter>` and `<Leave>` events to display accessible tooltips on icon-only controls.
