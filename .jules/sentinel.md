## 2026-09-09 - Parameterized SQL queries for caching user intent
**Vulnerability:** Missing database caching module in `ai_engine.py` risked unparameterized SQL operations when persisting user inputs in SQLite.
**Learning:** SQLite query parameterization using `?` placeholders prevents SQL injection vulnerabilities when querying and caching user intents.
**Prevention:** Always use parameterized SQL queries (`?` placeholders) for all database operations accepting user-provided strings.
