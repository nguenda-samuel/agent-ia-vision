## 2025-05-18 - Async UI Button Disabling and Tooltips in CustomTkinter

**Learning:** CustomTkinter icon-only buttons (`CTkButton`) lack accessible hover tooltips out-of-the-box and do not visually or functionally disable during async background threads unless explicitly updated.
**Action:** Always bind a lightweight `ToolTip` to icon-only controls and manage UI disabled states (`set_processing_ui`) around background processing steps to prevent double submission and improve accessibility.
