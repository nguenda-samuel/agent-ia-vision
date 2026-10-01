## 2026-09-04 - Parameterized SQLite Caching to Prevent SQL Injection
**Vulnerability:** Dynamic SQL string concatenation when querying or storing user intents in SQLite cache exposes the application to SQL injection attacks.
**Learning:** `ai_engine.py` relied on a missing `database` caching module, which requires parameterized queries for intent lookups and answer caching.
**Prevention:** Always use parameterized SQL query placeholders (`?` in sqlite3) instead of string concatenation or f-strings when handling user input.
