## 2026-09-18 - Parameterized Queries for SQLite Caching and .gitignore Whitelisting
**Vulnerability:** String-concatenated or unparameterized SQLite queries handling raw user input strings (`user_intent`) can lead to SQL injection vulnerabilities, allowing malicious inputs to bypass cache lookups or manipulate database state.
**Learning:** `ai_engine.py` imported `get_cached_answer` and `save_answer` from `database.py`, which was missing from the repository due to `.gitignore` wildcards (`*`) ignoring newly created files by default.
**Prevention:** Always use parameterized SQL placeholders (`?`) for SQLite queries when dealing with user inputs, and ensure any new security modules and test files are explicitly un-ignored in `.gitignore`.
