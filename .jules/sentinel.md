## 2026-09-04 - SQLite Parameterized Queries in AI Engine Cache
**Vulnerability:** `ai_engine.py` depended on a database cache module to store and retrieve user intents and AI responses. Missing input parameterization when querying local SQLite databases with unsanitized user intent strings creates SQL injection risks.
**Learning:** In projects using an explicit whitelist `.gitignore` pattern (`*`), new database modules or test files are ignored by git unless explicitly unignored with `!filename`.
**Prevention:** Always use parameterized SQLite queries (`?` placeholders) when caching user inputs. Un-ignore new security modules and tests in `.gitignore` when strict catch-all rule `*` is present.
