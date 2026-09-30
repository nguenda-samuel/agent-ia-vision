## 2026-09-04 - Parameterized Queries for SQLite Answer Cache
**Vulnerability:** Unsanitized string formatting in database queries when fetching or storing cached AI response strings (`user_intent`) could expose the SQLite database to SQL injection attacks.
**Learning:** Missing database cache module caused runtime import failures in `ai_engine.py`, and adding database functionality without parameterized queries creates injection risks when processing user-controlled prompts.
**Prevention:** Always use parameterized SQLite queries (`?`) instead of string formatting/concatenation when passing user input to database statements.
