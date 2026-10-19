import unittest
from unittest.mock import MagicMock
import sys
import types

# Mock database module if not present
if "database" not in sys.modules:
    db = types.ModuleType("database")
    db.get_cached_answer = lambda user_intent: None
    db.save_answer = lambda user_intent, answer: None
    sys.modules["database"] = db

from ai_engine import AIEngine, sanitize_error_message


class TestSecurityEnhancements(unittest.TestCase):

    def test_sanitize_error_message_api_key(self):
        raw_error = "API call failed: https://generativelanguage.googleapis.com/v1beta/models?key=AIzaSyA1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6"
        sanitized = sanitize_error_message(raw_error)
        self.assertNotIn("AIzaSyA1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6", sanitized)
        self.assertIn("[REDACTED]", sanitized)

    def test_sanitize_error_message_key_param(self):
        raw_error = "Error connecting with api_key=secret_token_12345 in response"
        sanitized = sanitize_error_message(raw_error)
        self.assertNotIn("secret_token_12345", sanitized)
        self.assertIn("[REDACTED]", sanitized)

    def test_user_intent_truncation_and_type_safety(self):
        mock_client = MagicMock()
        engine = AIEngine(gemini_client=mock_client)

        long_intent = "A" * 1500
        # Call process_screen_and_intent with no raw_screenshot
        res = engine.process_screen_and_intent(None, long_intent)
        self.assertEqual(res.get("action"), "none")

        # Test non-string user_intent handling
        res_non_str = engine.process_screen_and_intent(None, 12345)
        self.assertEqual(res_non_str.get("action"), "none")


if __name__ == "__main__":
    unittest.main()
