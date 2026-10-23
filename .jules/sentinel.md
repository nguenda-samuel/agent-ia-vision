## 2026-09-04 - Parameterized Queries for SQLite Cache Module
**Vulnerability:** Raw string formatting/concatenation in SQLite database queries allows SQL injection attacks when storing or querying cached user intents. Furthermore, missing module imports (`database`) can crash core AI engine processing.
**Learning:** `ai_engine.py` depended on a missing `database` module (`get_cached_answer` and `save_answer`). When implementing missing caching modules, SQLite queries must strictly use parameterized placeholders (`?`) to decouple SQL syntax from user-supplied inputs.
**Prevention:** Always use parameterized SQL statements (`?` bindings) for SQLite operations involving user intent inputs and un-ignore `database.py` in explicit-whitelist `.gitignore`.
