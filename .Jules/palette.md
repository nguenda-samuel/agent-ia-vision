## 2025-05-18 - Tooltips and Visual Loading States for Icon Buttons in CustomTkinter
**Learning:** Icon-only buttons in desktop GUIs (e.g., 📸 and 🚀) lack accessible text descriptions and visual state feedback during async execution, leaving users uncertain about button functionality and whether an operation is currently processing.
**Action:** Always attach hover tooltips (`CTkToolTip`) to icon-only buttons and explicitly toggle button `state` (`disabled`/`normal`) during async requests to provide visual affordance and prevent accidental duplicate submissions.
