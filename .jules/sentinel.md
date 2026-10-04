## 2026-10-01 - Missing Database Module and SQL Injection Risks
**Vulnerability:** `ai_engine.py` imported `get_cached_answer` and `save_answer` from `database`, but `database.py` was missing from the repository, causing runtime failures and opening risks for unparameterized raw SQL query implementations.
**Learning:** External or missing cache modules in local AI agent pipelines need parameterized SQLite implementations to safely handle user intent strings without risking SQL injection or runtime crashes.
**Prevention:** Always use parameterized SQL queries (`?`) for database operations handling user input and ensure modules required by core engine files exist in the repository.
