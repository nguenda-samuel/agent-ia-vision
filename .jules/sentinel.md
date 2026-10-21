## 2026-10-21 - SQLite Caching Module & Injection Prevention
**Vulnerability:** Missing `database.py` module relied upon by `ai_engine.py` for response caching risked SQL injection vulnerabilities if implemented with unparameterized string formatting.
**Learning:** `ai_engine.py` attempts to import `get_cached_answer` and `save_answer` from `database.py` to cache user intent responses.
**Prevention:** Always use parameterized SQLite queries (`?`) for database cache lookups and inserts to prevent SQL injection attacks.
