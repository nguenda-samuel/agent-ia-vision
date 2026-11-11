## 2026-09-22 - Parameterized Queries for Response Caching
**Vulnerability:** Raw string formatting or unparameterized queries in database operations can expose user intent inputs to SQL injection.
**Learning:** `ai_engine.py` imports `database` module functions (`get_cached_answer` and `save_answer`) to manage AI response caching. Without parameterized queries (`?`), user input passed via `user_intent` could manipulate SQLite queries.
**Prevention:** Always use parameterized SQL placeholders (`?`) rather than string concatenation or formatted strings when constructing SQLite queries.
