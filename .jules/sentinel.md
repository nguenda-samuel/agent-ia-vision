## 2026-09-28 - Parameterized SQLite Query Caching
**Vulnerability:** Missing database module `database.py` referenced by `ai_engine.py` risked unsafe string concatenation for user intent queries.
**Learning:** SQLite caching implementations handling raw `user_intent` strings must strictly use parameterized queries (`?` placeholders) rather than formatted strings to prevent SQL injection attacks.
**Prevention:** Always use parameterized SQL statements (`cursor.execute("SELECT ... WHERE key = ?", (val,))`) for SQLite operations.
