## 2026-09-24 - Parameterized Queries for SQLite Database Cache
**Vulnerability:** SQL injection risk in database caching mechanism and missing module dependency (`database.py`). Unsanitized input used in SQL queries can allow arbitrary SQL execution.
**Learning:** In projects with strict `.gitignore` whitelists (`*` ignored by default), untracked source files like `database.py` can easily be omitted from commits, causing runtime `ModuleNotFoundError` or vulnerable missing components.
**Prevention:** Always use parameterized SQL queries (`?`) for SQLite operations rather than string formatting/concatenation, and explicitly un-ignore newly added Python modules in `.gitignore`.
