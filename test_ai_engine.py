import json
import sys
import unittest
from unittest.mock import MagicMock

# Mock third-party dependencies not installed in the execution environment
sys.modules['google'] = MagicMock()
sys.modules['google.genai'] = MagicMock()
sys.modules['google.genai.types'] = MagicMock()
sys.modules['cv2'] = MagicMock()
sys.modules['numpy'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['imagehash'] = MagicMock()

from ai_engine import AIEngine


class TestAIEngine(unittest.TestCase):

    def setUp(self):
        self.mock_client = MagicMock()
        self.engine = AIEngine(gemini_client=self.mock_client)

    def test_cached_text_response_returns_from_memory(self):
        intent = "test intent"
        cached_result = {"action": "none", "text": "Cached response"}
        self.engine.memory.save_routine(
            screen_hash="", user_intent=intent, action_data=cached_result
        )

        result = self.engine.process_screen_and_intent(
            raw_screenshot=None, user_intent=intent
        )
        self.assertEqual(result, cached_result)

    def test_no_screenshot_and_no_cache_returns_error_dict(self):
        result = self.engine.process_screen_and_intent(
            raw_screenshot=None, user_intent="uncached intent"
        )
        self.assertEqual(result["action"], "none")
        self.assertIn("Désolé", result["text"])

    def test_input_validation_truncates_long_intent_and_strips_control_chars(self):
        long_intent = "A" * 600 + "\n\t\x00B"
        mock_screenshot = MagicMock()
        self.engine.privacy.redact_sensitive_data = MagicMock(return_value=mock_screenshot)

        mock_response = MagicMock()
        mock_response.text = json.dumps({"action": "none", "text": "Done"})
        self.mock_client.models.generate_content.return_value = mock_response

        self.engine.process_screen_and_intent(raw_screenshot=mock_screenshot, user_intent=long_intent)

        # Retrieve saved routine for sanitized intent
        expected_intent = "A" * 500
        saved = self.engine.memory.get_routine(screen_hash="", user_intent=expected_intent)
        self.assertIsNotNone(saved)

    def test_gemini_api_call_success_saves_to_memory(self):
        mock_screenshot = MagicMock()
        self.engine.privacy.redact_sensitive_data = MagicMock(return_value=mock_screenshot)

        mock_response = MagicMock()
        mock_response.text = json.dumps({"action": "click", "x": 100, "y": 200, "text": "Clicking button"})
        self.mock_client.models.generate_content.return_value = mock_response

        intent = "click login"
        result = self.engine.process_screen_and_intent(
            raw_screenshot=mock_screenshot, user_intent=intent
        )

        self.assertEqual(result["action"], "click")
        self.assertEqual(result["x"], 100)
        self.assertEqual(result["y"], 200)

        # Check memory saved
        saved = self.engine.memory.get_routine(screen_hash="", user_intent=intent)
        self.assertEqual(saved, result)


if __name__ == "__main__":
    unittest.main()
