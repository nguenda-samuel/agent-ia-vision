## 2026-09-04 - Parameterized Queries for SQLite Database Cache
**Vulnerability:** String concatenation or unparameterized queries in database interaction modules allow SQL injection (SQLi) when processing arbitrary user input (`user_intent`).
**Learning:** In applications using SQLite for intent response caching, user queries must be handled with parameterized SQL bindings (`?` placeholders) rather than string formatting.
**Prevention:** Always use parameterized placeholders (`?`) in `sqlite3` cursor executions for user inputs.
