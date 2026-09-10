## 2026-09-10 - SQL Injection Prevention in SQLite Cache
**Vulnerability:** Untrusted user input (`user_intent`) used in database cache queries could lead to SQL injection vulnerabilities if string formatting or concatenation is used.
**Learning:** When creating SQLite caching modules for user input, using string interpolation creates SQL injection risks. Furthermore, in repositories with explicit `.gitignore` whitelist patterns (`*` at root), newly added modules like `database.py` and `.jules/` must be un-ignored with `!`.
**Prevention:** Always use parameterized queries (`?`) for SQLite query parameters when working with user inputs, and ensure gitignore un-ignores essential python source files.
