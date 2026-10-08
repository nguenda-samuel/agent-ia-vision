## 2026-10-08 - Parameterized SQLite Queries for AI Cache

**Vulnerability:** Unsanitized user intent strings passed into SQLite database queries could allow SQL injection attacks when caching AI engine prompt responses.
**Learning:** `ai_engine.py` cached prompt responses in a SQLite database, but required a safe database module to handle arbitrary user inputs without string concatenation.
**Prevention:** Always use parameterized SQL placeholders (`?` in SQLite) when inserting or querying user input in database queries.
