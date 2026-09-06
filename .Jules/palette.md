# Palette's Journal

## 2025-05-20 - CustomTkinter Icon-Only Button Accessibility
**Learning:** CustomTkinter icon buttons (`CTkButton`) lack native hover tooltips or accessible screen reader hints for icon-only controls. Adding a lightweight Tkinter hover `ToolTip` window improves visual feedback and clarity for keyboard/mouse users without changing core layout parameters.
**Action:** Always attach a `ToolTip` to icon-only buttons (`btn_vision`, `btn_send`) in CustomTkinter UI.
