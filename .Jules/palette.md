# Palette's Journal - UX & Accessibility Learnings

## 2025-02-18 - Tooltips and Async Input Lock in CustomTkinter
**Learning:** Icon-only action buttons in CustomTkinter desktop applications lack native ARIA hints or tooltips. Combining a lightweight hover `ToolTip` with keyboard shortcut context (e.g. F9, Enter) improves accessibility and discoverability. Furthermore, disabling input fields and buttons during background AI tasks prevents accidental duplicate invocations and clearly signals processing state to the user.
**Action:** Always attach tooltips to icon-only controls and disable submit actions during async operations.
