## 2026-09-06 - Parameterized Database Cache and Whitelist Gitignore
**Vulnerability:** Missing database caching module referenced in `ai_engine.py` leading to potential SQL injection risks when handling un-sanitized user prompts (`user_intent`) in raw database queries if implemented incorrectly.
**Learning:** The project's `.gitignore` uses a default-deny wildcard (`*`) pattern which ignores all newly created files unless explicitly un-ignored with `!`.
**Prevention:** Always use parameterized SQLite queries (`?`) for database interactions and update `.gitignore` when adding new modules or tests so git tracks them properly.
