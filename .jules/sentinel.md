## 2026-08-30 - User Intent Prompt Injection and DoS Protection in LLM Agent
**Vulnerability:** Unsanitized and unbounded user input (`user_intent`) passed directly into LLM prompts without length validation or sanitization, exposing the agent to prompt injection and resource exhaustion (DoS).
**Learning:** LLM agents taking raw string inputs from users are vulnerable to prompt manipulation or large payload overhead if inputs are not validated, bounded, and sanitized before inclusion in prompt templates.
**Prevention:** Always enforce strict input length limits (e.g. max 500 characters), validate type/non-emptiness, and strip control/injection structures before interpolating user input into AI prompts.
