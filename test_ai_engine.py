import unittest
from ai_engine import sanitize_intent, AIEngine
from unittest.mock import MagicMock

class TestAIEngineSanitization(unittest.TestCase):

    def test_sanitize_intent_truncation(self):
        long_input = "a" * 1000
        result = sanitize_intent(long_input, max_length=500)
        self.assertEqual(len(result), 500)

    def test_sanitize_intent_control_characters(self):
        input_with_controls = "Click \n\r\t start \x00 button"
        result = sanitize_intent(input_with_controls)
        self.assertEqual(result, "Click  start  button")

    def test_sanitize_intent_non_string(self):
        self.assertEqual(sanitize_intent(None), "")
        self.assertEqual(sanitize_intent(12345), "")

    def test_process_screen_and_intent_sanitizes_input(self):
        mock_client = MagicMock()
        engine = AIEngine(gemini_client=mock_client)

        # Test text-only request with non-existent cache
        res = engine.process_screen_and_intent(raw_screenshot=None, user_intent="   \n\rTest intent   ")
        self.assertEqual(res["action"], "none")
        self.assertIn("analyser l'écran sans image", res["text"])

if __name__ == "__main__":
    unittest.main()
