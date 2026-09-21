# Sentinel Security Journal

## 2026-08-30 - SQLite Parameterized Queries Audit
**Vulnerability:** SQL injection risks can occur when user inputs are concatenated into database queries.
**Learning:** In `memory.py`, parameterized queries (`?`) were already used consistently with `sqlite3`.
**Prevention:** Ensure all future SQLite queries continue to use parameterized inputs rather than format strings or concatenation.
