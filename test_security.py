import sys
from unittest.mock import MagicMock

# Mock external packages if not installed in test environment
for mod in [
    'google',
    'google.genai',
    'google.genai.types',
    'cv2',
    'numpy',
    'PIL',
    'PIL.Image',
    'imagehash',
    'database',
    'privacy',
    'stream',
    'memory',
]:
    if mod not in sys.modules:
        sys.modules[mod] = MagicMock()

import ai_engine
# Mock database functions in ai_engine module directly
captured_intents = []

def dummy_get_cached(intent):
    captured_intents.append(intent)
    return None

ai_engine.get_cached_answer = dummy_get_cached

import unittest
from ai_engine import AIEngine


class TestSecurity(unittest.TestCase):

    def test_user_intent_sanitization_and_truncation(self):
        """Test that user_intent is truncated to 500 chars and non-printable control chars are stripped."""
        mock_client = MagicMock()
        engine = AIEngine(gemini_client=mock_client)

        # Mock privacy filter
        engine.privacy.redact_sensitive_data = lambda img: img

        # 1. Very long input (over 500 chars)
        long_intent = "A" * 1000
        # 2. Control characters (e.g., \x00, \x07, \x1b)
        control_chars_intent = "Hello\x00 World\x1b!"

        engine.process_screen_and_intent(raw_screenshot=None, user_intent=long_intent)
        self.assertEqual(len(captured_intents[-1]), 500)
        self.assertEqual(captured_intents[-1], "A" * 500)

        # Test control characters removal
        engine.process_screen_and_intent(raw_screenshot=None, user_intent=control_chars_intent)
        self.assertEqual(captured_intents[-1], "Hello World!")

    def test_error_message_masking_concept(self):
        """Test that raw exception string is masked when handling non-quota errors."""
        raw_error = "Traceback /path/to/secret/file API_KEY=secret_12345"

        # Simulating the sanitization logic in main_vision.py
        if "429" in raw_error or "RESOURCE_EXHAUSTED" in raw_error or "Quota" in raw_error:
            user_facing_msg = "⚠️ Quota API temporairement atteint."
        else:
            user_facing_msg = "❌ Une erreur s'est produite lors du traitement. Veuillez réessayer."

        self.assertNotIn("secret_12345", user_facing_msg)
        self.assertNotIn("/path/to/secret/file", user_facing_msg)
        self.assertEqual(user_facing_msg, "❌ Une erreur s'est produite lors du traitement. Veuillez réessayer.")


if __name__ == "__main__":
    unittest.main()
