## 2025-05-18 - Parameterized Queries for SQLite Caching
**Vulnerability:** Missing database caching module that was referenced by `ai_engine.py` causing `ModuleNotFoundError` and potential un-parameterized SQL injection risks in database query execution.
**Learning:** `ai_engine.py` referenced `from database import get_cached_answer, save_answer`, but `database.py` was missing from the repository.
**Prevention:** Always ensure database interactions use parameterized queries (`?` placeholders) with SQLite to eliminate SQL injection risks, and maintain test suites verifying parameterized inputs.
