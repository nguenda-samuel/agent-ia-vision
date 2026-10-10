## 2026-09-04 - SQLite Query Parameterization and Whitelist .gitignore Constraints
**Vulnerability:** Unsanitized string formatting in database queries introduces critical SQL injection risks when processing dynamic user input.
**Learning:** `ai_engine.py` depended on a database module caching user responses. When caching dynamic input like `user_intent`, raw query concatenation can expose SQLite databases to injection. Furthermore, the repository's `.gitignore` uses a default-ignore rule (`*`) requiring explicit whitelist rules (`!filename`) for newly added source or test files to be tracked by git.
**Prevention:** Always use parameterized SQLite queries (`?`) for database operations and ensure newly created files or tests are un-ignored in `.gitignore`.
