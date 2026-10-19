## 2026-10-19 - Parameterized Queries for SQLite Cache Module
**Vulnerability:** SQL injection risks and missing `database` module required by `ai_engine.py` when handling user intent strings for caching AI responses.
**Learning:** Raw string formatting/concatenation in SQL queries allows untrusted input (`user_intent`) to manipulate query execution. Moreover, explicit git ignore rules (`*`) require explicitly un-ignoring newly added Python files in `.gitignore`.
**Prevention:** Always use parameterized SQL queries (e.g. `cursor.execute("... VALUES (?, ?)", (val1, val2))`) for database access and un-ignore newly created critical module files in `.gitignore`.
