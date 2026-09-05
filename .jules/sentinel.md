## 2026-08-30 - Parameterized SQLite Queries for AI Cache
**Vulnerability:** Unsanitized user intent strings passed into SQL queries expose the application to SQL injection vulnerabilities in cache lookups.
**Learning:** `ai_engine.py` relies on `database.py` for response caching. In this repo, `.gitignore` uses an explicit whitelist strategy (`*` ignored by default), requiring new modules to be explicitly un-ignored.
**Prevention:** Always use parameterized queries (`?` placeholders in `sqlite3`) when querying or storing user inputs, and ensure newly added source/test files are explicitly un-ignored in `.gitignore`.
