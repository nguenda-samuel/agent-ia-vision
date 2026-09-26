import json
import os
import unittest
from unittest.mock import MagicMock, patch
import database
from ai_engine import AIEngine

TEST_DB_PATH = "test_ai_engine_cache.db"


class TestAIEngineDatabaseIntegration(unittest.TestCase):

    def setUp(self):
        self.original_db_path = database.DB_PATH
        database.DB_PATH = TEST_DB_PATH
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)

    def tearDown(self):
        database.DB_PATH = self.original_db_path
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)

    def test_process_screen_and_intent_uses_database_cache(self):
        mock_client = MagicMock()
        ai = AIEngine(gemini_client=mock_client)

        user_intent = "Open browser"
        cached_data = {"action": "none", "text": "Opening browser"}

        # Patch get_cached_answer in ai_engine module or save in TEST_DB_PATH
        with patch("ai_engine.get_cached_answer", side_effect=lambda intent: database.get_cached_answer(intent, db_path=TEST_DB_PATH)):
            # Save cached answer in DB using database module
            database.save_answer(user_intent, json.dumps(cached_data), db_path=TEST_DB_PATH)

            # Call process_screen_and_intent without screenshot (pure text query)
            result = ai.process_screen_and_intent(raw_screenshot=None, user_intent=user_intent)

            # Verify cached response returned without calling Gemini API
            self.assertEqual(result, cached_data)
            mock_client.models.generate_content.assert_not_called()


if __name__ == "__main__":
    unittest.main()
