## 2026-10-06 - Parameterized SQLite Queries for AI Engine Caching
**Vulnerability:** String concatenation or unparameterized queries in database caching layer can expose the application to SQL injection attacks via malicious user intents.
**Learning:** AI Engine queries user inputs directly; using parameterized queries (`?`) in SQLite prevents command execution or unauthorized data exposure.
**Prevention:** Always use parameterized SQL placeholders (`?`) rather than string interpolation or raw SQL formatting when executing queries.
