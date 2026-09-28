## 2026-09-04 - Parameterized Queries for SQLite Database Cache
**Vulnerability:** User intent strings passed into database cache lookup/storage could be vulnerable to SQL injection if formatted directly with string concatenation or f-strings.
**Learning:** `ai_engine.py` depended on `database.py` to cache AI answers, but `database.py` was absent and untracked in `.gitignore`.
**Prevention:** Always use parameterized SQLite queries (`?` positional bindings in `sqlite3`) when querying or updating SQLite database tables with user input. Un-ignore newly created security components in `.gitignore`.
