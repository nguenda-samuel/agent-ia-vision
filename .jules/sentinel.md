## 2026-09-04 - Parameterized Queries for SQLite Cache

**Vulnerability:** `ai_engine.py` expected a `database` module with caching helper functions (`get_cached_answer` and `save_answer`), which if implemented via string formatting would introduce SQL injection risks when handling user intent strings containing SQL metacharacters (e.g. `' OR '1'='1`).

**Learning:** Missing modules referenced by core components can lead to runtime failures or insecure fallback implementations. Using parameterized queries (`?` placeholders in `sqlite3`) ensures user intent text is safely escaped by the database engine regardless of input content.

**Prevention:** Always use parameterized SQL queries (`?`) when constructing SQLite statements with dynamic input.
