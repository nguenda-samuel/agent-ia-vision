import os
import unittest
from unittest.mock import MagicMock
from ai_engine import AIEngine
import database

TEST_DB_PATH = "cache.db"


class TestAIEngineIntegration(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)

    def tearDown(self):
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)

    def test_text_only_query_cache_hit(self):
        mock_client = MagicMock()
        engine = AIEngine(gemini_client=mock_client)

        user_intent = "How do I print a document?"
        cached_json = '{"action": "none", "text": "Press Ctrl+P"}'

        database.save_answer(user_intent, cached_json, db_path=TEST_DB_PATH)

        # process_screen_and_intent with raw_screenshot=None should hit database cache
        result = engine.process_screen_and_intent(raw_screenshot=None, user_intent=user_intent)

        self.assertEqual(result, {"action": "none", "text": "Press Ctrl+P"})
        # Verify gemini client was NOT called due to cache hit
        mock_client.models.generate_content.assert_not_called()


if __name__ == "__main__":
    unittest.main()
