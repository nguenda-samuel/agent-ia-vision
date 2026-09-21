## 2026-09-04 - SQLite Parameterization in Answer Cache
**Vulnerability:** Raw string formatting/concatenation in SQLite query construction allows SQL injection when caching or fetching AI user intents.
**Learning:** `ai_engine.py` depended on `database.py` for caching user intents and AI responses. Using parameterized queries (`?` place holders) ensures user intent strings containing SQL constructs are safely escaped.
**Prevention:** Always use parameterized SQL queries with tuple parameter bindings (`cursor.execute(sql, (param,))`) rather than string interpolation or formatting.
