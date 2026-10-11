## 2026-09-04 - SQLite Parameterized Query Protection in AI Caching
**Vulnerability:** String concatenation in SQL queries allows SQL injection attacks when user intent strings are queried or stored in SQLite database caches.
**Learning:** `ai_engine.py` depended on a missing `database` module (`get_cached_answer` and `save_answer`), which requires safe query parameterized implementations to safely interact with SQLite without exposing raw SQL construction risks.
**Prevention:** Always use parameterized SQL placeholders (`?`) in `sqlite3` cursor executions for user inputs instead of formatted strings or string concatenation.
