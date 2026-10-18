import sys
import unittest
from unittest.mock import MagicMock

# Mock database module before importing AIEngine
sys.modules['database'] = MagicMock()

from ai_engine import AIEngine


class TestAIEngineSanitization(unittest.TestCase):

    def setUp(self):
        self.mock_client = MagicMock()
        self.engine = AIEngine(gemini_client=self.mock_client)

    def test_sanitize_user_intent_normal(self):
        intent = "  clique   sur le bouton  "
        sanitized = self.engine._sanitize_user_intent(intent)
        self.assertEqual(sanitized, "clique sur le bouton")

    def test_sanitize_user_intent_empty_or_none(self):
        self.assertEqual(
            self.engine._sanitize_user_intent(""),
            "Assistance et guidage sur l'écran"
        )
        self.assertEqual(
            self.engine._sanitize_user_intent(None),
            "Assistance et guidage sur l'écran"
        )

    def test_sanitize_user_intent_length_limit(self):
        long_intent = "a" * 1000
        sanitized = self.engine._sanitize_user_intent(long_intent)
        self.assertEqual(len(sanitized), 500)

    def test_sanitize_user_intent_control_characters(self):
        intent = "hello\x00world\x07!"
        sanitized = self.engine._sanitize_user_intent(intent)
        self.assertEqual(sanitized, "helloworld!")


if __name__ == "__main__":
    unittest.main()
