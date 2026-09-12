## 2026-09-04 - SQLite Database Caching and Gitignore Whitelisting
**Vulnerability:** User intent strings in database queries risk SQL injection if concatenated directly into query strings, and untracked database modules cause import failures when `.gitignore` uses global `*` exclusion rules.
**Learning:** The project's `.gitignore` uses a default catch-all rule `*`, ignoring all newly created source files and subdirectories like `.jules/` unless explicitly unignored with `!`.
**Prevention:** Always use parameterized SQL queries (`?`) for SQLite operations and ensure newly added Python modules, test files, and security journal paths are explicitly unignored in `.gitignore`.
