## 2026-09-04 - Parameterized Queries for SQLite Database Caching
**Vulnerability:** Unsanitized user intent strings passed into SQLite queries when retrieving or saving cached AI engine responses could lead to SQL injection vulnerabilities.
**Learning:** `ai_engine.py` depended on a missing `database` module (`get_cached_answer` and `save_answer`). When creating caching modules for user input, raw string formatting or concatenation should never be used for SQL parameters.
**Prevention:** Always use parameterized SQL placeholders (`?` in SQLite) when inserting or querying user-provided inputs in database queries. Ensure `.gitignore` explicit whitelist rules (`*`) explicitly un-ignore newly added core source and test files.
