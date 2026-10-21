## 2025-10-21 - CustomTkinter Tooltips and Async Action States
**Learning:** CustomTkinter icon-only buttons (`📸`, `🚀`) lack built-in accessibility descriptions and tooltips. Adding a lightweight `CTkToolTip` wrapper provides necessary hover context for keyboard and screen reader users without requiring extra UI packages. Toggling button states during processing prevents duplicate submissions while giving visual feedback.
**Action:** Always wrap icon-only buttons with `CTkToolTip` and ensure submit buttons update their state during async operations.
