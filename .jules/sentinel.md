## 2026-09-01 - Parameterized Queries for Database Caching
**Vulnerability:** Missing database caching module (`database.py`) imported by `ai_engine.py` posed a risk of improper string formatting/concatenation SQL injection when caching user input intent.
**Learning:** `ai_engine.py` expected `get_cached_answer` and `save_answer` functions to query SQLite. Without parameterized queries, user inputs with single quotes or SQL keywords could corrupt queries or cause SQL injection vulnerabilities.
**Prevention:** Always use parameterized SQL placeholders (`?`) with SQLite `cursor.execute(sql, params)` instead of string formatting or concatenation when interacting with database stores.
