## 2026-09-04 - SQL Injection Risk with SQLite Database Cache
**Vulnerability:** Raw string formatting/concatenation or unparameterized queries when storing and querying user intent in SQLite cache can lead to SQL injection attacks.
**Learning:** `ai_engine.py` depended on `database.py` for response caching (`get_cached_answer` and `save_answer`), which was missing or susceptible to SQL injection if user inputs (`user_intent`) are interpolated directly into SQL queries.
**Prevention:** Always use parameterized SQL queries (`?` placeholders in SQLite) when inserting or querying user-provided inputs in database operations.
