## 2026-09-03 - Git Whitelist Ignore Strategy
**Vulnerability:** Unsanitized user intent strings in AI response caching could lead to SQL injection vulnerabilities when executing database queries.
**Learning:** The project uses an explicit whitelist strategy in `.gitignore` (`*` ignores all files by default). Newly added source files or test modules (such as `database.py` and `test_database.py`) will be ignored by git unless explicitly un-ignored in `.gitignore`.
**Prevention:** Always update `.gitignore` with `!filename` when introducing new source or test files to prevent accidental omission from source control.
