## 2026-09-02 - Gitignore Whitelist Hiding Missing Security Modules
**Vulnerability:** A missing `database.py` module broke application caching and imported dependencies because `.gitignore` uses a default-deny wildcard (`*`), causing untracked modules to be omitted.
**Learning:** In projects with default-deny `.gitignore` rules, newly added or refactored security modules must be explicitly whitelisted (e.g., `!database.py`) to prevent breaking code imports and missing security controls in remote repository clones.
**Prevention:** Always check `.gitignore` when adding new security modules or test files to ensure explicit un-ignore rules exist.
