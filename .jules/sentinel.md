## 2026-10-30 - Safe Exception Handling and Input Length Validation in ActionMemory

**Vulnerability:** Unbounded input lengths and missing exception handling on JSON parsing in `ActionMemory` methods (`save_routine`, `get_routine`).
**Learning:** SQLite queries with parameterized placeholders prevent SQL injection, but unbounded string arguments and unhandled JSON decode exceptions in DB read operations leave the application vulnerable to DoS, memory exhaustion, and crash risks on corrupted data.
**Prevention:** Always enforce strict type checking, maximum input lengths on text fields, and wrap `json.loads` calls in safe try-except blocks when reading stored payloads.
