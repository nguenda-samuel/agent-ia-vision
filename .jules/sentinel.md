## 2026-08-30 - SQL Injection Prevention in Database Caching
**Vulnerability:** Unimplemented or dynamically constructed SQLite database queries on user intent strings in AI caching modules can lead to SQL Injection.
**Learning:** `ai_engine.py` imported caching functions (`get_cached_answer`, `save_answer`) from `database`, but the database module was missing and required parameterized query implementation (`?` placeholders).
**Prevention:** Always use parameterized SQL placeholders (`?` in sqlite3) when querying or storing raw user input/intents.
