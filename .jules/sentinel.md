## 2025-03-30 - Missing Database Cache Module and SQL Injection Prevention
**Vulnerability:** Missing database caching module referenced by `ai_engine.py` could lead to unstable database interactions or unsafe query construction when storing and retrieving user prompt intents in cache.
**Learning:** `ai_engine.py` relied on `get_cached_answer` and `save_answer` from a `database` module. Caching arbitrary user intents requires strict parameterized query handling for SQLite.
**Prevention:** Always use parameterized SQL queries (`?` placeholders in SQLite) when saving or querying user inputs to prevent SQL injection attacks.
