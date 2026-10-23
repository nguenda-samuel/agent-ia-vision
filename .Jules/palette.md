## 2025-05-18 - Hover Tooltips for Icon-Only Buttons in CustomTkinter
**Learning:** Icon-only buttons (such as `🚀` and `📸`) in CustomTkinter desktop applications lack native accessibility tooltips, leaving keyboard and screen reader / mouse hover users without clear visual context.
**Action:** Attach a lightweight `Toplevel` `ToolTip` bound to `<Enter>` and `<Leave>` events on all icon-only or quick action buttons to enhance micro-UX clarity and accessibility.
