## 2026-11-11 - CustomTkinter Composite Widget Hover Event Binding for Tooltips
**Learning:** In CustomTkinter, composite widgets like `CTkButton` encapsulate inner `CTkCanvas` and `tk.Label` child widgets. Binding `<Enter>` and `<Leave>` only to the container widget causes hover events to be absorbed by child elements, making tooltips unreliable.
**Action:** Recursively bind hover events (`<Enter>`, `<Leave>`, `<ButtonPress>`) to all children in `widget.winfo_children()` with `add="+"` so tooltips fire consistently across the entire button surface.
