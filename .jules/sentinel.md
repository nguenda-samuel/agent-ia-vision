## 2026-09-11 - Safe SQLite Caching to Prevent SQL Injection

**Vulnerability:** `ai_engine.py` imports `get_cached_answer` and `save_answer` from `database.py`, but `database.py` was missing from the repository. Without parameterized queries, dynamic SQL construction for caching user intents could lead to SQL injection vulnerabilities.
**Learning:** Missing database abstraction layer modules can cause runtime failures or lead to unsafe inline query implementations if added hastily without parameters.
**Prevention:** Always implement database interactions using parameterized queries (`?` in SQLite) and maintain module abstractions in version control.
