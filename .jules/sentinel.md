# Sentinel Security Journal

## 2025-10-05 - SQL Injection Prevention and Error Message Sanitization
**Vulnerability:** Missing database caching module referenced by `ai_engine.py` and unhandled exception details being appended directly to user UI.
**Learning:** Raw exception strings in GUI apps can expose sensitive API tokens or stack details. Always sanitize error messages shown to users and use parameterized SQL queries (`?`) for database caching.
**Prevention:** Always sanitize exception messages before user display and enforce parameterized queries in SQLite operations.
