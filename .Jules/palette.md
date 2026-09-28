## 2025-05-18 - Accessibility Tooltips & Action States for Tkinter Icon Buttons
**Learning:** CustomTkinter icon-only buttons lack native DOM ARIA attributes; adding hover-triggered `ToolTip` windows gives immediate accessible context for icon buttons, while disabling action buttons during background processing prevents duplicate requests and signals loading state.
**Action:** Always attach lightweight `ToolTip` popups to icon-only buttons in Tkinter GUIs and ensure async triggers temporarily disable trigger widgets.
