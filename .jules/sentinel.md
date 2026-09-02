## 2026-09-02 - Parameterized SQLite Queries for Cache DB
**Vulnerability:** Unsanitized string formatting in database queries can lead to SQL injection vulnerabilities when handling user inputs (such as user intents).
**Learning:** `ai_engine.py` relies on `database.py` (`get_cached_answer` and `save_answer`) to cache AI responses based on `user_intent`. Passing unescaped user input into raw SQL queries allows SQL injection attacks.
**Prevention:** Always use parameterized SQL queries (`?` placeholders in SQLite) when inserting or querying user-provided strings.
