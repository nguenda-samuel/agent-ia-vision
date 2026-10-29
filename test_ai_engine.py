import unittest
from unittest.mock import MagicMock, patch

from PIL import Image

from ai_engine import AIEngine


class TestAIEngineIntegration(unittest.TestCase):

    @patch("ai_engine.get_cached_answer")
    def test_process_screen_and_intent_uses_cached_answer(self, mock_get_cached):
        mock_get_cached.return_value = '{"action": "none", "text": "Cached response"}'
        mock_client = MagicMock()
        engine = AIEngine(gemini_client=mock_client)

        result = engine.process_screen_and_intent(
            raw_screenshot=None, user_intent="What is on screen?"
        )

        mock_get_cached.assert_called_once_with("What is on screen?")
        self.assertEqual(result, {"action": "none", "text": "Cached response"})

    @patch("ai_engine.save_answer")
    @patch.object(AIEngine, "__init__", lambda self, gemini_client: None)
    def test_process_screen_and_intent_saves_answer(self, mock_save):
        engine = AIEngine(gemini_client=None)
        engine.client = MagicMock()
        engine.privacy = MagicMock()
        dummy_img = Image.new("RGB", (100, 100))
        engine.privacy.redact_sensitive_data.return_value = dummy_img

        mock_response = MagicMock()
        mock_response.text = '{"action": "none", "text": "Generated response"}'
        engine.client.models.generate_content.return_value = mock_response

        result = engine.process_screen_and_intent(
            raw_screenshot=dummy_img, user_intent="Analyze screen"
        )

        self.assertEqual(result, {"action": "none", "text": "Generated response"})
        mock_save.assert_called_once_with(
            "Analyze screen", '{"action": "none", "text": "Generated response"}'
        )


if __name__ == "__main__":
    unittest.main()
