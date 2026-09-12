## 2026-08-30 - Missing Database Cache Module & SQL Injection Prevention
**Vulnerability:** `ai_engine.py` imported `get_cached_answer` and `save_answer` from `database`, but `database.py` was missing from the repository, causing module import failures and exposing potential SQL injection risks if non-parameterized raw SQL was used.
**Learning:** Cache operations against SQLite database must always use parameterized queries (`?` placeholders) and graceful error handling to prevent SQL injection vulnerabilities and stack trace disclosure.
**Prevention:** Ensure database interactions strictly use parameter binding rather than string formatting/concatenation, and catch database exceptions to avoid leaking internal errors.
