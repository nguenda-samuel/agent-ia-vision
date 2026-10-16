# Sentinel Security Journal

## 2026-08-30 - Explicit Git Whitelist & Parameterized SQLite Cache
**Vulnerability:** Missing database caching module (`database.py`) in `ai_engine.py` coupled with un-parameterized SQL query risk when storing user intent queries in SQLite cache.
**Learning:** An explicit catch-all `*` in `.gitignore` silently omitted `database.py` during previous development. When caching dynamic AI queries or user inputs in SQL databases, missing parameterization creates high SQL injection vulnerability.
**Prevention:** Always whitelist newly created source and test files in `.gitignore` when catch-all patterns are used, and mandate parameterized queries (`?`) for all SQLite database operations handling user prompt data.
