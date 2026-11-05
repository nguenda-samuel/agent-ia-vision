## 2026-09-04 - Parameterized Queries for AI Cache Database
**Vulnerability:** Missing database cache module caused runtime import errors and potential SQL injection vulnerability if queries were constructed using string formatting.
**Learning:** `ai_engine.py` depended on `database.py`'s `get_cached_answer` and `save_answer` helper functions for caching user intent responses.
**Prevention:** Always use parameterized SQL queries (`?` placeholders in SQLite) when inserting or querying user intent strings into cache databases, preventing SQL injection vulnerabilities.
