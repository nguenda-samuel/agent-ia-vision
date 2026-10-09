import json
import os
import unittest
from unittest.mock import MagicMock

from database import get_cached_answer, save_answer
import ai_engine

TEST_DB = "test_cache.db"


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def tearDown(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_save_and_get_cached_answer(self):
        intent = "ouvrir le navigateur"
        answer = '{"action": "click", "x": 100, "y": 200, "text": "Ouverture"}'

        self.assertIsNone(get_cached_answer(intent, db_path=TEST_DB))

        save_answer(intent, answer, db_path=TEST_DB)
        cached = get_cached_answer(intent, db_path=TEST_DB)

        self.assertEqual(cached, answer)

    def test_sql_injection_prevention(self):
        # Save a legitimate response first
        save_answer("intent_normal", "normal_answer", db_path=TEST_DB)

        # Attempt SQL injection as user intent
        injection_intent = "' OR '1'='1"
        save_answer(injection_intent, "malicious_or_injected_answer", db_path=TEST_DB)

        # Querying normal intent should return normal answer, not injected answer
        self.assertEqual(get_cached_answer("intent_normal", db_path=TEST_DB), "normal_answer")

        # Querying injection payload should return malicious answer specifically tied to that exact payload key, not leak other entries
        self.assertEqual(get_cached_answer(injection_intent, db_path=TEST_DB), "malicious_or_injected_answer")

        # Querying a non-existent injection string should safely return None, not match all records
        self.assertIsNone(get_cached_answer("' OR 1=1 --", db_path=TEST_DB))

    def test_ai_engine_database_integration(self):
        # Test that AIEngine utilizes database functions imported from database.py
        mock_client = MagicMock()
        engine = ai_engine.AIEngine(gemini_client=mock_client)

        intent = "quelle heure est-il?"
        # Save cache entry
        expected_dict = {"action": "none", "text": "Il est 12:00"}
        save_answer(intent, json.dumps(expected_dict))

        # Process intent without raw_screenshot -> should hit cache
        result = engine.process_screen_and_intent(raw_screenshot=None, user_intent=intent)
        self.assertEqual(result, expected_dict)


if __name__ == "__main__":
    unittest.main()
