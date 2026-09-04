## 2026-08-31 - SQL Injection in Database Caching
**Vulnerability:** Unsanitized user inputs could lead to SQL injection when retrieving or saving cached AI engine responses in SQLite.
**Learning:** `ai_engine.py` expected a `database.py` module with caching functions `get_cached_answer` and `save_answer`.
**Prevention:** Always use parameterized SQLite queries (`?` placeholders) instead of string formatting/concatenation for database operations.
