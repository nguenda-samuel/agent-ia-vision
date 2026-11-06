## 2026-11-06 - Parameterized Queries for Response Caching
**Vulnerability:** Constructing database queries using unsanitized string formatting or unparameterized queries when caching user intent strings can expose the application to SQL injection (SQLi).
**Learning:** `ai_engine.py` calls `database.py` functions (`get_cached_answer` and `save_answer`) using raw `user_intent` input. Without parameterized queries (`?`), an adversary or untrusted user input could alter query logic or execute arbitrary SQLite statements.
**Prevention:** Always use parameterized SQL placeholders (`?`) in SQLite queries for both `SELECT` and `INSERT/UPDATE` operations, validate user inputs, and ensure any newly created modules are explicitly tracked in `.gitignore`.
