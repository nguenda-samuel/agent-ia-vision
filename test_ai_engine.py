import json
import unittest
from unittest.mock import MagicMock

from ai_engine import AIEngine
import database


class TestAIEngineDatabaseIntegration(unittest.TestCase):

    def test_cached_answer_retrieval(self):
        mock_client = MagicMock()
        engine = AIEngine(gemini_client=mock_client)

        user_intent = "test intent"
        expected_response = {"action": "none", "text": "Cached response"}

        # Save cached answer in database
        database.save_answer(user_intent, json.dumps(expected_response))

        # Call process_screen_and_intent with raw_screenshot=None
        result = engine.process_screen_and_intent(raw_screenshot=None, user_intent=user_intent)

        self.assertEqual(result, expected_response)


if __name__ == "__main__":
    unittest.main()
