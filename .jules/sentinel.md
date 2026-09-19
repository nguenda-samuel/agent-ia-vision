## 2026-09-19 - Parameterized Queries for SQLite Database Cache
**Vulnerability:** SQL injection hazard and missing module error in database caching layer when storing or querying user intent strings.
**Learning:** `ai_engine.py` imports `database` module which was missing due to `.gitignore` patterns ignoring all untracked files by default (`*`). Any dynamic SQL query string construction with user intent input poses SQL injection risks.
**Prevention:** Always use parameterized SQL queries (`?` placeholders in SQLite) and ensure new source files are explicitly un-ignored in `.gitignore`.
