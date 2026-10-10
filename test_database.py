import os
import unittest
from unittest.mock import MagicMock
from database import get_cached_answer, save_answer, DEFAULT_DB_PATH
from ai_engine import AIEngine

TEST_DB_PATH = "test_cache.db"


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        for db in (TEST_DB_PATH, DEFAULT_DB_PATH):
            if os.path.exists(db):
                os.remove(db)

    def tearDown(self):
        for db in (TEST_DB_PATH, DEFAULT_DB_PATH):
            if os.path.exists(db):
                os.remove(db)

    def test_save_and_get_cached_answer(self):
        user_intent = "What is the capital of France?"
        cached_response = '{"text": "Paris"}'

        save_answer(user_intent, cached_response, db_path=TEST_DB_PATH)
        result = get_cached_answer(user_intent, db_path=TEST_DB_PATH)

        self.assertEqual(result, cached_response)

    def test_get_nonexistent_cached_answer(self):
        result = get_cached_answer("Nonexistent query", db_path=TEST_DB_PATH)
        self.assertIsNone(result)

    def test_sql_injection_prevention(self):
        # Attempt SQL injection payload in user_intent
        sqli_intent = "' OR '1'='1"
        save_answer(sqli_intent, "Malicious response", db_path=TEST_DB_PATH)

        # Querying an exact different intent should return None, not "Malicious response"
        self.assertIsNone(get_cached_answer("normal_intent", db_path=TEST_DB_PATH))

        # Querying the exact sqli string safely returns the stored response
        self.assertEqual(
            get_cached_answer(sqli_intent, db_path=TEST_DB_PATH),
            "Malicious response",
        )

    def test_ai_engine_database_cache_integration(self):
        mock_client = MagicMock()
        ai = AIEngine(gemini_client=mock_client)

        user_intent = "Hello AI"
        # Save cache entry in default DB used by AIEngine
        save_answer(user_intent, '{"action": "none", "text": "Cached Hello"}')

        # process_screen_and_intent without raw_screenshot should return cached answer
        result = ai.process_screen_and_intent(None, user_intent)
        self.assertEqual(result, {"action": "none", "text": "Cached Hello"})


if __name__ == "__main__":
    unittest.main()
