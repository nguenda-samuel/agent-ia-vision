## 2026-08-30 - Missing Module Tracking and SQL Injection Prevention in SQLite Cache
**Vulnerability:** The `ai_engine` module attempted to import `get_cached_answer` and `save_answer` from `database.py`, but `database.py` was missing from the repository because `.gitignore` ignored all files by default (`*`). Without proper SQLite parameterization, caching user intent queries risked SQL injection attacks.
**Learning:** Repositories using wildcard `.gitignore` rules (`*`) prevent new source files from being committed unless explicitly allowed via `!filename.py`.
**Prevention:** Always check `.gitignore` when adding new modules, and always use parameterized queries (`?`) for database operations handling user input.
