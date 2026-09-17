## 2026-09-17 - Safe Database Caching and Whitelist .gitignore Rules
**Vulnerability:** Missing database caching module caused runtime crashes and risk of unsafe SQL query string formatting for user intents.
**Learning:** The project .gitignore uses an explicit whitelist pattern where all unlisted files are ignored by default (`*`). When adding new python modules or test files, they must be explicitly un-ignored in `.gitignore` (with `!filename`) so git tracks them.
**Prevention:** Always use parameterized SQL queries (`?`) in SQLite interactions and ensure newly added module and test files are explicitly un-ignored in `.gitignore`.
