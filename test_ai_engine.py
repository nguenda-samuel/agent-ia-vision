import os
import unittest
from unittest.mock import MagicMock
from PIL import Image

# Ensure database is available before importing ai_engine
import database
from ai_engine import AIEngine

TEST_DB = "test_ai_engine_cache.db"


class TestAIEngineDatabaseIntegration(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)
        database.DB_PATH = TEST_DB

    def tearDown(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)
        database.DB_PATH = "cache.db"

    def test_cache_hit_without_screenshot(self):
        intent = "What is this?"
        cached_json = '{"action": "none", "text": "Cached answer"}'
        database.save_answer(intent, cached_json, db_path=TEST_DB)

        mock_client = MagicMock()
        engine = AIEngine(gemini_client=mock_client)

        result = engine.process_screen_and_intent(raw_screenshot=None, user_intent=intent)
        self.assertEqual(result, {"action": "none", "text": "Cached answer"})
        mock_client.models.generate_content.assert_not_called()


if __name__ == "__main__":
    unittest.main()
