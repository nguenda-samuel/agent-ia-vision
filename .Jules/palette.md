## 2026-09-04 - CustomTkinter Icon-Only Buttons & Processing Feedback

**Learning:** Icon-only CTkButtons in CustomTkinter lack accessible text descriptions by default, leaving visual-only icons ambiguous to users. Combining a lightweight `CTkToolTip` hovering popover with state transitions (`state="disabled"` and updating button text to `⏳`) during asynchronous background tasks provides clear accessibility descriptions and prevents duplicate input triggers.
**Action:** Always pair CustomTkinter icon-only buttons with hover tooltips (`CTkToolTip`) and disable input controls with visual status feedback during async operations.
