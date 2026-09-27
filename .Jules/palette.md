## 2025-05-10 - Tooltips and ARIA-like descriptions for CustomTkinter icon buttons
**Learning:** CustomTkinter desktop applications often use icon-only buttons (like `📸` or `🚀`) without tooltip text or accessible hover feedback, making their intent unclear to screen reader users or mouse hoverers.
**Action:** Always wrap icon-only CTkButton widgets with a dedicated lightweight tooltip listener (`CTkToolTip`) bound to `<Enter>`/`<FocusIn>` and `<Leave>`/`<FocusOut>` to provide clear visual context and screen-reader hover assistance.
