## 2026-09-04 - SQLite Parameterized Query Caching

**Vulnerability:** String concatenation/unparameterized SQL queries in database modules allow SQL injection when handling user input like `user_intent`.
**Learning:** `ai_engine.py` depended on an external `database` module (`get_cached_answer` and `save_answer`). Missing or unsafe database implementations risk SQL injection if input is directly formatted into SQL strings.
**Prevention:** Always use parameterized SQL queries (`?` placeholders with parameter tuples) in SQLite operations to sanitize user inputs and prevent SQL injection.
