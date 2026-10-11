import json
import os
import unittest
from unittest.mock import MagicMock

from ai_engine import AIEngine
from database import get_cached_answer, save_answer, DB_PATH


class TestAIEngineDatabaseIntegration(unittest.TestCase):

    def tearDown(self):
        if os.path.exists(DB_PATH):
            try:
                os.remove(DB_PATH)
            except OSError:
                pass

    def test_cached_text_response_retrieval(self):
        user_intent = "bonjour"
        expected_response = {
            "action": "none",
            "text": "Bonjour ! Comment puis-je vous aider ?",
        }
        save_answer(user_intent, json.dumps(expected_response))

        engine = AIEngine(gemini_client=MagicMock())
        result = engine.process_screen_and_intent(
            raw_screenshot=None, user_intent=user_intent
        )

        self.assertEqual(result, expected_response)


if __name__ == "__main__":
    unittest.main()
