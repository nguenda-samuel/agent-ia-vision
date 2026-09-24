## 2026-08-30 - User Input Sanitization for LLM Prompts
**Vulnerability:** Unsanitized user intent strings were passed directly into Gemini LLM prompts and database cache functions, creating risks of prompt injection and token-exhaustion DoS attacks.
**Learning:** External LLM prompt construction using raw user inputs can accept overly large strings or control characters that increase token usage costs or disrupt prompt framing.
**Prevention:** Always sanitize and truncate user input before embedding in LLM prompts or caching layers.
