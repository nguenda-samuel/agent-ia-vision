## 2026-09-04 - Parameterized Queries for SQLite Cache
**Vulnerability:** SQL injection risks and missing database cache module in AI engine query processing.
**Learning:** `ai_engine.py` imported `get_cached_answer` and `save_answer` from `database`, but `database.py` was missing from the repository. Raw string queries on cached database entries can lead to SQL injection vulnerabilities when user input contains quotes or SQL control characters.
**Prevention:** Always use parameterized SQL queries (`?` placeholders in SQLite) when inserting or retrieving user-supplied inputs from SQLite databases.
