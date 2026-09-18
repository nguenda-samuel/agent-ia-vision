## 2026-09-18 - Safe SQLite Database Caching & SQL Injection Prevention
**Vulnerability:** Missing database module `database.py` imported in `ai_engine.py`, risking unsafe SQL string formatting or missing caching layer if implemented incorrectly.
**Learning:** When adding SQLite database caching for AI response caching, parameterizing queries (`?`) prevents SQL injection attacks when processing untrusted user prompts/intents. Also, explicit `.gitignore` whitelist configuration requires adding new `.py` files and journal entries (`.jules/sentinel.md`) explicitly to `.gitignore`.
**Prevention:** Always use parameterized SQL queries (`?` in SQLite) for database operations involving user input, and ensure new repository files are explicitly whitelisted in `.gitignore`.
