## 2026-09-17 - Missing Database Cache Module & Parameterized SQLite Queries
**Vulnerability:** `ai_engine.py` imported `database.get_cached_answer` and `save_answer` which did not exist, causing runtime crash. Database caching required safe parameterized SQL queries to prevent SQL injection.
**Learning:** The project used an explicit `.gitignore` whitelist (`*` ignored by default), meaning new modules like `database.py` must be explicitly unignored (`!database.py`).
**Prevention:** Ensure new database modules use parameterized queries (`?`) and are explicitly added to `.gitignore`.
