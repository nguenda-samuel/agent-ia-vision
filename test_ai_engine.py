import unittest
from ai_engine import AIEngine


class TestAIEngineSanitization(unittest.TestCase):

    def test_sanitize_intent_basic(self):
        intent = "   Clique sur le bouton  "
        sanitized = AIEngine._sanitize_intent(intent)
        self.assertEqual(sanitized, "Clique sur le bouton")

    def test_sanitize_intent_quotes_and_slashes(self):
        intent = 'Say "Hello\\World"'
        sanitized = AIEngine._sanitize_intent(intent)
        self.assertEqual(sanitized, 'Say "Hello\\World"')

    def test_sanitize_intent_control_characters(self):
        intent = "Hello\x00\x07World\nNew Line"
        sanitized = AIEngine._sanitize_intent(intent)
        self.assertEqual(sanitized, "HelloWorld\nNew Line")

    def test_sanitize_intent_length_limit(self):
        long_intent = "a" * 1000
        sanitized = AIEngine._sanitize_intent(long_intent, max_length=500)
        self.assertEqual(len(sanitized), 500)

    def test_sanitize_intent_empty(self):
        self.assertEqual(AIEngine._sanitize_intent(""), "")
        self.assertEqual(AIEngine._sanitize_intent(None), "")


if __name__ == "__main__":
    unittest.main()
