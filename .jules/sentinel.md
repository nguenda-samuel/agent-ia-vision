## 2026-09-04 - SQLite Parameterized Caching & Module Isolation
**Vulnerability:** Unsanitized user intent string interpolated into SQLite queries for answer caching, leading to SQL injection vulnerability and runtime `ModuleNotFoundError` when `database` module was missing.
**Learning:** `ai_engine.py` relies on `database.py` for answer caching. Ensuring SQL queries use parameterized placeholders (`?`) prevents injection while maintaining performance and API stability.
**Prevention:** Always use parameterized queries for all SQLite interactions and ensure referenced module dependencies are present in the codebase.
