## 2026-09-11 - SQL Injection Prevention in SQLite Cache Layer
**Vulnerability:** User intent strings passed to AI response cache functions could lead to SQL injection if concatenated directly into dynamic SQL queries.
**Learning:** `ai_engine.py` imports `database` module functions `get_cached_answer` and `save_answer` for caching text answers. If `database.py` is omitted or uses raw string formatting, it creates module import errors and security vulnerabilities.
**Prevention:** Always use parameterized SQLite queries (`?`) for user inputs and ensure database cache modules are properly committed and tested.
