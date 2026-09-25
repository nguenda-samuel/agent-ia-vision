## 2025-09-25 - [SQL Injection Prevention in SQLite Caching]
**Vulnerability:** Unsanitized user intent inputs when executing SQLite database queries for response caching could allow SQL injection.
**Learning:** `ai_engine.py` imported `database.py` for caching user responses, but the database helper module was missing and required parameterization.
**Prevention:** Always use parameterized SQL queries (`?` placeholders with `sqlite3`) for user inputs instead of string formatting or concatenation.
