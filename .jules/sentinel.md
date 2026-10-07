## 2026-10-07 - Safe SQLite Query Parameterization in Database Caching
**Vulnerability:** Unsanitized user intent queries passed directly into database queries expose SQLite databases to SQL injection attacks and data leakage.
**Learning:** `ai_engine.py` relied on a missing `database.py` module for caching responses based on `user_intent` strings. Building cache query implementations requires strict parameterization to safely handle arbitrary user inputs.
**Prevention:** Always use parameterized SQL placeholders (`?` bindings in SQLite) rather than f-strings or string concatenation when querying or updating database rows.
