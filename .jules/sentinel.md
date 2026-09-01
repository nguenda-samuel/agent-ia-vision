## 2026-08-31 - SQLite Parameterized Queries & Whitelist .gitignore Pitfalls
**Vulnerability:** Missing database module caused by default wildcard ignore rules (`*`) in `.gitignore`, combined with potential SQL injection vulnerabilities if user queries are interpolated into raw SQL strings.
**Learning:** In repositories with whitelist-style `.gitignore` configurations (`*` at top-level), newly created modules like `database.py` and test files will be silently ignored unless explicitly un-ignored (`!database.py`).
**Prevention:** Always check `.gitignore` whitelist patterns when introducing new python source files or modules, and strictly enforce parameterized queries (`?`) for all SQLite database operations.
