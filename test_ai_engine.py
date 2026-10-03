import unittest
from unittest.mock import MagicMock
import os

os.environ["GEMINI_API_KEY"] = "dummy_key"

from ai_engine import AIEngine
from database import save_answer


class TestAIEngineCacheIntegration(unittest.TestCase):

    def test_cached_text_response_without_screenshot(self):
        mock_client = MagicMock()
        engine = AIEngine(gemini_client=mock_client)

        intent = "test_text_intent"
        cached_val = '{"action": "none", "text": "cached_text_result"}'
        save_answer(intent, cached_val)

        result = engine.process_screen_and_intent(raw_screenshot=None, user_intent=intent)

        self.assertEqual(result, {"action": "none", "text": "cached_text_result"})
        mock_client.models.generate_content.assert_not_called()


if __name__ == "__main__":
    unittest.main()
