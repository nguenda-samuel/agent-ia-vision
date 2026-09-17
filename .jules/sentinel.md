## 2026-09-17 - Safe SQLite Database Caching with Parameterized Queries
**Vulnerability:** Missing database module `database.py` referenced in `ai_engine.py` for caching AI responses created potential SQL injection risks if implemented via string formatting or dynamic SQL queries on user inputs (`user_intent`).
**Learning:** Even local SQLite database caches handling user intent strings must strictly use parameterized queries (`?` syntax in Python's `sqlite3`) to prevent query manipulation and injection flaws.
**Prevention:** Always use parameterized SQL placeholders (`?` placeholders) when passing dynamic parameters into SQL statements, even for local caching modules.
