## 2026-09-04 - Safe SQLite Database Caching with Parameterized Queries
**Vulnerability:** Unsanitized user inputs in SQL queries risk SQL injection attacks when storing or retrieving cached AI responses.
**Learning:** `ai_engine.py` caches AI outputs based on user prompts (`user_intent`). Using raw string formatting or concatenation in SQLite queries allows malicious inputs to alter database operations.
**Prevention:** Always use parameterized SQLite queries (`?` placeholders) when passing user-supplied input into database functions.
