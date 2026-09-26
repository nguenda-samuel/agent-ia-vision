## 2026-09-26 - Parameterized Database Queries for Answer Caching
**Vulnerability:** Unparameterized queries in database caching modules can expose SQLite databases to SQL injection attacks via user prompt inputs.
**Learning:** `ai_engine.py` imports `database.py` for answer caching based on `user_intent`. Implementing `database.py` with parameterized queries (`?` placeholders) prevents SQL injection and provides a safe database caching implementation.
**Prevention:** Always use parameterized SQLite queries (`?` placeholders) when passing untrusted user input to `cursor.execute()`.
