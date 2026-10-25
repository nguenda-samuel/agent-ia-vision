## 2026-10-25 - Parameterized SQLite Cache to Prevent SQL Injection

**Vulnerability:** The AI engine module (`ai_engine.py`) imported a missing `database` module for caching answers (`get_cached_answer` and `save_answer`), which caused runtime crashes and risk of unsafe database queries if user-provided intent strings were formatted unsafely.
**Learning:** SQLite database operations storing user intent queries must use parameterized binding rather than string formatting/concatenation to ensure user input cannot modify SQL query structure. Additionally, explicit `.gitignore` whitelisting required un-ignoring `database.py`.
**Prevention:** Always use `?` parameter placeholders in SQLite queries for dynamic parameters and update `.gitignore` when adding required source files in whitelisted repositories.
