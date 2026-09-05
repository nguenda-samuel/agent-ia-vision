## 2026-09-05 - Explicit Whitelist .gitignore Silently Ignores New Security Code
**Vulnerability:** New security modules and database files were omitted from Git tracking because `.gitignore` uses an explicit whitelist pattern (`*` ignored by default).
**Learning:** `ai_engine.py` depended on `database.py` which was missing from version control due to the default ignore rule `*`. When adding new files in this codebase, they are ignored by Git unless explicitly un-ignored with `!` rules in `.gitignore`.
**Prevention:** Whenever adding new files (modules, tests, documentation), ensure `.gitignore` explicitly includes rules (e.g. `!database.py`) to un-ignore them.
