## 2026-10-06 - Safe SQLite database caching to prevent SQL Injection
**Vulnerability:** Missing database caching module referenced by `ai_engine.py` leading to potential SQL injection risks if unsanitized user intent strings were interpolated directly into raw SQLite queries.
**Learning:** The database module was missing from the repository root because the root `.gitignore` file contains a wildcard default ignore (`*`), ignoring untracked Python files unless explicitly un-ignored.
**Prevention:** Always use parameterized SQL queries (`?`) for database operations with user input, and ensure new security modules are un-ignored in `.gitignore`.
