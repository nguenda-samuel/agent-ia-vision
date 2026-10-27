## 2026-09-04 - Parameterized SQLite database cache module
**Vulnerability:** Missing database module `database.py` imported by `ai_engine.py` risked unparameterized raw SQL query implementation leading to SQL injection when caching AI responses based on `user_intent`.
**Learning:** `ai_engine.py` imports `get_cached_answer` and `save_answer` from `database.py`. Without parameterized placeholders (`?`), untrusted string inputs in `user_intent` can alter query structure or manipulate cached data.
**Prevention:** Always use parameterized SQL query placeholders (`?` in sqlite3) instead of string formatting or concatenation when inserting or retrieving user input in database queries.
