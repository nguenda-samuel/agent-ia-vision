## 2026-08-30 - Sensitive Information Leakage in GUI Error Messages
**Vulnerability:** Raw exception strings (`err_msg`) were rendered directly into the user-facing CustomTkinter chat interface during unhandled application errors in `VisionAssistantApp.autonomous_agent_step`.
**Learning:** Exception messages can contain sensitive credentials, database connection strings, or system paths. Exposing them in the UI violates secure error handling standards.
**Prevention:** Always log raw exception details internally or to secure audit logs, while returning sanitized generic error messages to user-facing interfaces.
