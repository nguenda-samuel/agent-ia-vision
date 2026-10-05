## 2026-09-01 - Prevent SQL injection in AI Engine response caching database
**Vulnerability:** User inputs (`user_intent`) passed directly into database cache queries pose SQL injection risks if constructed via raw SQL string concatenation or f-strings.
**Learning:** `ai_engine.py` imported cache functions `get_cached_answer` and `save_answer` from `database.py`. Missing or improperly written SQL queries using string formatting accept arbitrary user input strings.
**Prevention:** Always use parameterized SQL queries (`?` placeholders) when querying or storing user-controlled inputs in SQLite tables.
