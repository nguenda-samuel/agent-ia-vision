## 2026-09-04 - Parameterized Queries for SQLite Cache
**Vulnerability:** SQL injection risks and missing dependency module in AI response caching mechanism.
**Learning:** `ai_engine.py` imported `get_cached_answer` and `save_answer` from `database`, but `database.py` was uncommitted/missing. Implementing raw or string-interpolated SQL queries for string matching in local SQLite caches can expose application databases to SQL injection attacks if user inputs are untrusted.
**Prevention:** Always use parameterized SQL queries (`?` placeholders in SQLite) when inserting or querying database rows based on user input or user intent strings. Ensure newly added required database modules are tracked in `.gitignore`.
