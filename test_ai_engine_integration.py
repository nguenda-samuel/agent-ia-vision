import json
import os
import unittest
from unittest.mock import MagicMock
from ai_engine import AIEngine
from database import init_db, save_answer

TEST_DB = "cache.db"


class TestAIEngineDatabaseIntegration(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)
        init_db(TEST_DB)

    def tearDown(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_process_screen_and_intent_uses_database_cache(self):
        mock_client = MagicMock()
        engine = AIEngine(gemini_client=mock_client)

        user_intent = "bonjour"
        cached_data = {"action": "none", "text": "Bonjour ! Comment puis-je vous aider ?"}
        save_answer(user_intent, json.dumps(cached_data), db_path=TEST_DB)

        # Call process_screen_and_intent with raw_screenshot=None
        result = engine.process_screen_and_intent(raw_screenshot=None, user_intent=user_intent)

        # Should retrieve from DB cache without calling Gemini API client
        self.assertEqual(result, cached_data)
        mock_client.models.generate_content.assert_not_called()


if __name__ == "__main__":
    unittest.main()
