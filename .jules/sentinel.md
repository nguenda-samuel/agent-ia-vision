## 2026-09-07 - SQLite Parameterized Database Cache Implementation
**Vulnerability:** `ai_engine.py` imported `database.get_cached_answer` and `save_answer`, but `database.py` was missing, causing module import failure or unsafe SQL execution risk if implemented with string formatting.
**Learning:** `database.py` was missing from the repository root due to a strict `.gitignore` whitelist (`*`). Adding new Python modules requires updating `.gitignore` with `!filename.py`.
**Prevention:** Always use parameterized SQLite queries (`?` placeholders) and ensure all whitelist-based `.gitignore` files are updated when creating new source/test files.
