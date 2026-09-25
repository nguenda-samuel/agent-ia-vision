# Sentinel Security Journal

## 2026-09-04 - SQLite Parameterized Cache Query and Git Whitelist
**Vulnerability:** User-controlled prompts (`user_intent`) queried or stored in SQLite database without parameterization risk SQL injection attacks and database query errors. Additionally, missing `database.py` module in git tracking due to default-deny `.gitignore` rules breaks `ai_engine.py`.
**Learning:** `ai_engine.py` imports `database` for answer caching. SQLite queries must always use parameterized placeholders (`?`) instead of string interpolation. Furthermore, in projects with a root wildcard `.gitignore` (`*`), new source modules and test files must be explicitly un-ignored (`!database.py`) to prevent being omitted from source control.
**Prevention:** Always use parameterized SQL queries (`?`) in database helper functions and explicitly add newly added files to `.gitignore` when a wildcard ignore rule is in place.
