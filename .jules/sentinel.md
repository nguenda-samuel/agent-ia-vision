## 2026-09-04 - Parameterized SQLite database cache
**Vulnerability:** Missing database cache dependency (`database.py`) in `ai_engine.py` causing import errors, with potential SQL injection risk if unparameterized queries were used.
**Learning:** `ai_engine.py` relies on `get_cached_answer` and `save_answer` from `database.py`. Using explicit parameterized queries (`?`) in SQLite prevents string-concatenation SQL injection vulnerabilities when caching user input intents.
**Prevention:** Always use parameterized SQL queries (`?`) when passing user inputs to SQLite database operations.
