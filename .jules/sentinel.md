## 2026-10-03 - Parameterized SQLite Caching
**Vulnerability:** Unsanitized user intents interpolated into SQL queries could allow SQL injection attacks or cause runtime errors when special characters are queried/stored in local cache tables.
**Learning:** `ai_engine.py` depended on a missing `database.py` caching layer. Caching user input string requests in SQLite without parameterized queries (`?`) introduces SQL injection vectors.
**Prevention:** Always use parameterized SQL queries (`?` place-holders with parameter tuples) in SQLite operations rather than string concatenation or formatting.
