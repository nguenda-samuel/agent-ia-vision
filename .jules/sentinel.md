## 2026-09-02 - SQLite Database Cache SQL Injection Prevention
**Vulnerability:** `ai_engine.py` imports `database.py` to cache AI responses based on `user_intent`, but `database.py` was missing from the repository.
**Learning:** If query parameters like `user_intent` are directly formatted into SQL strings without parameterization (`?`), malicious user input could trigger SQL injection attacks.
**Prevention:** Always use parameterized SQLite queries (`?`) for database lookups and updates in `database.py`.
