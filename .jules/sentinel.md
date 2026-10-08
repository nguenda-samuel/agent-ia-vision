## 2026-10-08 - SQLite Database Cache Parameterization
**Vulnerability:** `ai_engine.py` imported `database.py` for caching AI responses, but `database.py` was missing from the repository. Unhandled or raw SQL queries on cached user intents can introduce SQL injection vulnerabilities.
**Learning:** Missing helper modules like `database.py` break core functionality (`ai_engine.py` imports `get_cached_answer` and `save_answer`), and user input (`user_intent`) passed directly to SQLite queries without parameterization allows query manipulation.
**Prevention:** Always use parameterized SQL queries (`?` placeholder in SQLite) for user inputs and ensure database utility files are tracked and un-ignored in `.gitignore`.
