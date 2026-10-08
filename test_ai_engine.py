import json
import os
import unittest
from unittest.mock import MagicMock

import database
from ai_engine import AIEngine


class TestAIEngineCacheIntegration(unittest.TestCase):

    def setUp(self):
        self.test_db = "cache.db"
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_text_only_cached_answer_retrieval(self):
        intent = "bonjour"
        expected_dict = {
            "action": "none",
            "text": "Bonjour ! Comment puis-je vous aider ?",
        }
        database.save_answer(intent, json.dumps(expected_dict))

        mock_client = MagicMock()
        ai = AIEngine(gemini_client=mock_client)

        result = ai.process_screen_and_intent(
            raw_screenshot=None, user_intent=intent
        )

        self.assertEqual(result, expected_dict)
        mock_client.models.generate_content.assert_not_called()


if __name__ == "__main__":
    unittest.main()
