## 2026-08-31 - Explicit Whitelist .gitignore and Parameterized SQLite Queries
**Vulnerability:** Unsanitized user inputs in SQLite cache queries could lead to SQL injection attacks if string formatting were used. Additionally, new modules were untracked due to `*` default ignore rule in `.gitignore`.
**Learning:** This codebase uses a strict `*` wildcard in `.gitignore` requiring explicit exception rules (`!file.py`). Creating a missing module (`database.py`) also required updating `.gitignore`.
**Prevention:** Always use parameterized `?` placeholders for SQLite queries and update `.gitignore` exceptions when adding new source or test files.
