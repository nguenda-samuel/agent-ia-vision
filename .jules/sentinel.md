## 2026-09-10 - Parameterized SQLite Cache Module
**Vulnerability:** Missing database caching module referenced by `ai_engine.py` leading to `ModuleNotFoundError` or potential SQL injection risk if implemented via string formatting.
**Learning:** SQL queries on user-supplied intent strings must always use parameterized placeholders (`?`) rather than string interpolation or raw SQL execution.
**Prevention:** Always use `sqlite3` parameterized queries (`cursor.execute("... ?", (param,))`) for data storage and retrieval in database operations.
