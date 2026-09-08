## 2026-09-08 - SQLite Parameterized Query for Cache Database

**Vulnerability:**
The `ai_engine` module imported `database` functions (`get_cached_answer` and `save_answer`) for response caching. Without parameterized queries, raw string interpolation in SQL queries with user input (`user_intent`) introduces SQL injection vulnerabilities.

**Learning:**
Always use parameterized queries (`?` placeholders in SQLite) when inserting or querying user input into SQLite databases. Furthermore, in repositories with a restrictive `.gitignore` (wildcard `*` ignore pattern), newly added modules such as `database.py` and test/journal files must be explicitly un-ignored (`!database.py`, `!.jules/`) in `.gitignore`.

**Prevention:**
Enforce parameterized SQL queries across all database access functions and ensure `.gitignore` rules are updated when creating new source files.
