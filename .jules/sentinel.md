## 2026-09-01 - Secure SQLite Cache Implementation for AI Engine
**Vulnerability:** `ai_engine.py` imported `get_cached_answer` and `save_answer` from an absent `database` module. In SQLite caching layers taking untrusted user intent strings, unparameterized query interpolation allows SQL injection attacks.
**Learning:** SQLite query execution must strictly utilize parameterized query syntax (`?`) and handle non-string inputs safely to eliminate SQL injection vectors.
**Prevention:** Always parameterize SQLite queries with `?` placeholders and validate input data types.
