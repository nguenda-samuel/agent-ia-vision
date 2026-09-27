## 2026-09-04 - SQLite Parameterized Queries and `.gitignore` Exclusion
**Vulnerability:** Missing database module dependency and potential SQL injection vulnerability in cache database queries.
**Learning:** Root `.gitignore` had a default `*` rule that ignored newly added security modules (`database.py`) unless explicitly un-ignored (`!database.py`).
**Prevention:** Always ensure new security modules and tests are explicitly un-ignored in `.gitignore` and use parameterized queries (`?` bindings) for all SQLite operations.
