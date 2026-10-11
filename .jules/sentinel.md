## 2026-09-04 - Parameterized SQLite database caching
**Vulnerability:** SQL injection risk or missing database module when caching AI responses with user-provided intent strings.
**Learning:** `ai_engine.py` imports `database.py` for caching user intents and responses. Using parameterized queries in SQLite (`?` placeholders) prevents SQL injection attacks when user intent strings contain SQL syntax.
**Prevention:** Always use parameterized queries (`?` placeholders in SQLite) when inserting or retrieving user-controlled data rather than string formatting.
