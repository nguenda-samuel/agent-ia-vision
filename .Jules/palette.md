## 2026-10-01 - Async Processing Button State Management
**Learning:** In CustomTkinter applications with async background workers, leaving action buttons in normal active state during long-running background tasks allows repetitive user clicks and creates visual confusion without indication that a request is already in progress.
**Action:** Always wrap background processing states in a central helper (`set_processing_state`) that explicitly sets button `state="disabled"` when starting and schedules `state="normal"` on the main GUI thread upon completion or cancellation.
