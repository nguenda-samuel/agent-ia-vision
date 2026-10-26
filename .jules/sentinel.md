## 2026-10-26 - Information Leakage via GUI Exception Handling
**Vulnerability:** Raw exception objects `str(e)` rendered directly in CustomTkinter chat bubbles exposed internal API keys, request headers, and stack traces.
**Learning:** Exception handling in desktop AI assistant applications must decouple internal exception handling from user-facing UI messages to avoid leaking credentials or environment data.
**Prevention:** Always return generic user-friendly messages in UI event handlers and keep raw exception details in internal logs only.
