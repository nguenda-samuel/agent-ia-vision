## 2026-09-04 - Parameterized Queries for SQLite Database Cache
**Vulnerability:** Unsanitized user inputs in SQL queries risk SQL injection vulnerabilities and missing database module caused runtime failures in `ai_engine.py`.
**Learning:** Using raw string formatting or concatenation when building SQL queries can allow untrusted user input to break query structure or execute unauthorized SQL logic.
**Prevention:** Always use parameterized queries (`?` placeholders in SQLite) when building SQL statements to keep user data strictly separate from code execution.
