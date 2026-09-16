## 2026-09-15 - Missing Database Cache Module & Whitelisted .gitignore
**Vulnerability:** `ai_engine.py` imported `get_cached_answer` and `save_answer` from a non-existent `database` module, which caused a runtime import error and potential insecure query patterns when re-implementing cache modules.
**Learning:** The project's `.gitignore` uses a global wildcard `*` with explicit un-ignores (`!filename.py`). New modules like `database.py` and `test_database.py` must be explicitly un-ignored in `.gitignore` to be committed to git.
**Prevention:** Always verify `.gitignore` patterns when adding new files to repos using explicit whitelist rules, and ensure parameterization for any new database caching routines.
