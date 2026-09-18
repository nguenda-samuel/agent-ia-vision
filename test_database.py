import json
import os
import unittest
from unittest.mock import MagicMock

from ai_engine import AIEngine
from database import DB_PATH, get_cached_answer, save_answer

TEST_DB = "test_cache.db"


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)

    def tearDown(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)

    def test_save_and_get_cached_answer(self):
        intent = "Open music player"
        response = '{"action": "click", "x": 100, "y": 200, "text": "Clicking player"}'

        save_answer(intent, response, db_path=TEST_DB)
        cached = get_cached_answer(intent, db_path=TEST_DB)

        self.assertEqual(cached, response)

    def test_sql_injection_prevention(self):
        # Attempt SQL injection attack via user intent
        malicious_intent = "Open music' OR '1'='1"
        save_answer(malicious_intent, "malicious_result", db_path=TEST_DB)

        # Ensure looking up benign intent doesn't return malicious_result due to injection
        result = get_cached_answer("Open music", db_path=TEST_DB)
        self.assertIsNone(result)

        # Ensure looking up exact malicious intent works safely as a literal string
        result_exact = get_cached_answer(malicious_intent, db_path=TEST_DB)
        self.assertEqual(result_exact, "malicious_result")

    def test_ai_engine_cache_integration(self):
        # Verify that AIEngine uses database.get_cached_answer
        mock_client = MagicMock()
        engine = AIEngine(gemini_client=mock_client)

        intent = "text query"
        cached_payload = json.dumps({"action": "none", "text": "Cached response text"})
        save_answer(intent, cached_payload)

        # Calling process_screen_and_intent without screenshot should hit database cache
        result = engine.process_screen_and_intent(raw_screenshot=None, user_intent=intent)
        self.assertEqual(result, {"action": "none", "text": "Cached response text"})
        mock_client.models.generate_content.assert_not_called()


if __name__ == "__main__":
    unittest.main()
