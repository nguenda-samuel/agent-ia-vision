## 2026-09-14 - Parameterized Queries for SQLite Database Caching

**Vulnerability:** Constructing SQL queries using dynamic string formatting or concatenation with user input (like `user_intent`) creates SQL injection vulnerabilities.

**Learning:** In `ai_engine.py`, caching logic relied on a missing `database` module. Implementing caching without parameterized queries could allow malicious user input to execute arbitrary SQL or manipulate query logic.

**Prevention:** Always use parameterized SQL queries (`?` placeholders in SQLite) when passing dynamic parameters to database queries.
