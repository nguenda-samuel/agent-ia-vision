## 2026-10-25 - Parameterized Queries for SQLite Database Caching

**Vulnerability:** Missing database caching module referenced by `ai_engine.py` resulted in application crash and risk of unparameterized string formatting for SQL queries on user intent strings.
**Learning:** SQLite database queries using string interpolation (`f"SELECT ... '{user_input}'"`) create SQL injection risks when user input contains quotes or SQL statements. Missing database dependencies also disrupt AI engine execution.
**Prevention:** Always use parameterized SQL queries (`?` syntax in Python `sqlite3`) when querying or saving dynamic user input.
