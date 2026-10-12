import unittest
from unittest.mock import MagicMock
from ai_engine import AIEngine
from database import save_answer


class TestAIEngineIntegration(unittest.TestCase):

    def test_process_screen_and_intent_uses_database_cache(self):
        mock_client = MagicMock()
        engine = AIEngine(gemini_client=mock_client)

        user_intent = "Open Settings"
        expected_json = '{"action": "none", "text": "Opening Settings"}'

        # Populate cache
        save_answer(user_intent, expected_json)

        # Call engine without screenshot -> should return cached answer from database.py
        result = engine.process_screen_and_intent(raw_screenshot=None, user_intent=user_intent)

        self.assertEqual(result, {"action": "none", "text": "Opening Settings"})
        mock_client.models.generate_content.assert_not_called()


if __name__ == "__main__":
    unittest.main()
