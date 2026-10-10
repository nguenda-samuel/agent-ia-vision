## 2026-10-10 - Parameterized SQLite Queries for AI Engine Response Cache
**Vulnerability:** SQL injection risks arise when dynamically constructing SQL queries with user intents in SQLite database caching routines.
**Learning:** `ai_engine.py` imports `get_cached_answer` and `save_answer` from `database.py` to cache AI responses based on raw user input (`user_intent`). Without parameterized queries (`?` placeholders), malicious user prompt inputs could alter query logic or cause syntax errors/injection.
**Prevention:** Always use parameterized SQL placeholders (`?`) in `sqlite3` calls (`cursor.execute(sql, params)`). Never concatenate raw strings or format strings into SQL query definitions.
