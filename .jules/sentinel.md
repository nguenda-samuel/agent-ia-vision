## 2026-09-03 - Missing Database Cache Module & Potential SQL Injection Risk
**Vulnerability:** `ai_engine.py` imported `database.get_cached_answer` and `database.save_answer`, but `database.py` was missing from the repository, creating a runtime failure and an opportunity for unsafe SQL string concatenation when caching user intents.
**Learning:** Cache layers handling arbitrary user input must strictly utilize parameterized SQL queries to avoid SQL injection when caching queries or prompts.
**Prevention:** Always implement database interactions using parameterized placeholders (`?`) and ensure new modules and tests are un-ignored in `.gitignore`.
