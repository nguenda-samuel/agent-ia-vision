## 2026-03-31 - Unsanitized Exception Leakage in Desktop Chat UI
**Vulnerability:** Unexpected runtime exceptions caught in `VisionAssistantApp.autonomous_agent_step` leaked internal exception message strings directly to the user-facing chat UI (`append_to_chat`).
**Learning:** Returning or appending `str(e)` directly to end-user UI elements exposes sensitive internal details (e.g. database credentials, file paths, external API details) when unexpected runtime failures occur.
**Prevention:** Always catch and log detailed internal exceptions server-side/console-side, while presenting safe, non-sensitive error messages to end-user interfaces.
