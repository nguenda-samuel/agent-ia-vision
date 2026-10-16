## 2026-09-04 - Parameterized SQLite Caching & Runtime DB Path Evaluation
**Vulnerability:** Unsanitized string formatting in database queries allows SQL injection attacks when caching user prompts (`user_intent`) in `ai_engine.py`.
**Learning:** In addition to using parameterized SQLite queries (`?`), default function arguments bound at module import time (`db_path: str = DB_PATH`) prevent test suites from overriding `DB_PATH` dynamically, risking test side-effects on production DB files.
**Prevention:** Use parameterized queries for all user inputs (`?`) and resolve `DB_PATH` dynamically at runtime (`if db_path is None: db_path = DB_PATH`) to ensure secure SQL execution and clean test isolation.
