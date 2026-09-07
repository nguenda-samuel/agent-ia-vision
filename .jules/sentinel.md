## 2026-09-07 - Gitignore Whitelist Pattern for New Security Modules
**Vulnerability:** New security modules and database files were ignored by default because `.gitignore` uses an explicit wildcard block (`*`) with whitelist overrides (`!filename`).
**Learning:** Any new python source file, test file, or directory added to the repository will be silently untracked by Git unless explicitly unignored in `.gitignore`.
**Prevention:** Always check `.gitignore` rules when adding new security files or tests in this repository and add explicit `!filename` entries.
