## 2026-10-13 - Database Cache SQL Injection and Git Whitelist Pattern
**Vulnerability:** Unsanitized user intent queries used in database caching can lead to SQL injection attacks or application crashes, and missing files can be accidentally excluded by `*` whitelist patterns in `.gitignore`.
**Learning:** `ai_engine.py` imports `database.py` for response caching. Using raw string formatting in database queries allows arbitrary SQL execution via malicious user intent inputs. Additionally, `.gitignore` uses an explicit whitelist strategy (`*`), ignoring new security modules unless explicitly negated (`!`).
**Prevention:** Always use parameterized SQLite queries (`?` positional parameters) for data parameters and explicitly declare new modules in `.gitignore`.
