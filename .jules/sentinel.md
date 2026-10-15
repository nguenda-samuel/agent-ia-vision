## 2026-09-04 - Parameterized SQLite Caching to Prevent SQL Injection

**Vulnerability:**
The `ai_engine` module relied on an uncommitted/missing `database` module (`from database import get_cached_answer, save_answer`). Creating a naive implementation with string formatting in SQL queries could allow SQL injection vulnerabilities via untrusted user prompt strings.

**Learning:**
Database caching layer components that receive user inputs (such as screen intent prompts) must always use parameterized SQL queries (`?` place holders in SQLite).

**Prevention:**
Always use parameterized queries (`cursor.execute(sql, params)`) rather than string interpolation or concatenation when querying or updating SQLite databases. Ensure newly created security modules and tests are unignored in `.gitignore`.
