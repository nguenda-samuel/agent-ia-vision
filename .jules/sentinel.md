## 2026-09-08 - Parameterized SQLite Database Cache and Gitignore Whitelist
**Vulnerability:** Missing database module `database.py` referenced in `ai_engine.py` leading to potential SQL injection vulnerabilities if user prompts (`user_intent`) are improperly handled in raw SQL queries.
**Learning:** The codebase relies on a strict default-deny `.gitignore` pattern (`*`), requiring newly created source and test files to be explicitly un-ignored (`!database.py`, `!test_database.py`, `!.jules/sentinel.md`).
**Prevention:** Always use parameterized SQLite queries (`?`) for database operations to prevent SQL injection, and update `.gitignore` when adding new files to ensure they are tracked.
