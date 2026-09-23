## 2025-05-10 - Safe SQLite Database Caching & Explicit Gitignore Tracking
**Vulnerability:** Missing database module required by `ai_engine.py` causing runtime failure, and potential SQL injection vulnerability if string formatting/concatenation were used for user intent cache lookups.
**Learning:** The project .gitignore uses an explicit whitelist pattern (`*` ignored by default); newly created source files like `database.py` and `test_database.py` must be explicitly un-ignored in `.gitignore` or git will ignore them.
**Prevention:** Always use parameterized SQL queries (`?` placeholders) when handling user inputs in SQLite, and remember to update `.gitignore` when adding new files to whitelisted repositories.
