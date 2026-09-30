# Palette's Journal - Micro-UX & Accessibility Learnings

## 2026-09-30 - Tooltips and Async Button States in CustomTkinter
**Learning:** Icon-only buttons in desktop GUIs (like 📸 and 🚀) require visible hover tooltips to clarify their purpose for mouse and screen reader users. Additionally, async operations must explicitly set interactive buttons to `state="disabled"` on submission to prevent duplicate triggers and provide immediate feedback.
**Action:** Always attach tooltips to icon-only buttons and toggle button `state` ("disabled"/"normal") during async operations.
