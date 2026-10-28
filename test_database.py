import os
import sqlite3
import unittest
from unittest.mock import MagicMock

from database import get_cached_answer, save_answer

TEST_DB = "test_cache.db"


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def tearDown(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_save_and_get_cached_answer(self):
        intent = "Open music player"
        response = '{"action": "click", "x": 100, "y": 200, "text": "Opening music"}'

        self.assertIsNone(get_cached_answer(intent, db_path=TEST_DB))

        save_answer(intent, response, db_path=TEST_DB)

        cached = get_cached_answer(intent, db_path=TEST_DB)
        self.assertEqual(cached, response)

    def test_update_existing_cache_entry(self):
        intent = "Search web"
        initial_res = '{"action": "none", "text": "Searching..."}'
        updated_res = '{"action": "none", "text": "Search completed"}'

        save_answer(intent, initial_res, db_path=TEST_DB)
        self.assertEqual(get_cached_answer(intent, db_path=TEST_DB), initial_res)

        save_answer(intent, updated_res, db_path=TEST_DB)
        self.assertEqual(get_cached_answer(intent, db_path=TEST_DB), updated_res)

    def test_sql_injection_prevention(self):
        sqli_intent = "test' OR '1'='1"
        sqli_response = '{"action": "none", "text": "Injected"}'

        save_answer(sqli_intent, sqli_response, db_path=TEST_DB)

        self.assertEqual(get_cached_answer(sqli_intent, db_path=TEST_DB), sqli_response)
        self.assertIsNone(get_cached_answer("normal_intent", db_path=TEST_DB))

    def test_ai_engine_database_cache_integration(self):
        """Verify that AIEngine imports database module and retrieves/saves cached answers safely."""
        from ai_engine import AIEngine

        mock_client = MagicMock()
        engine = AIEngine(gemini_client=mock_client)

        intent = "Play music"
        cached_json = '{"action": "click", "x": 50, "y": 50, "text": "Playing"}'

        # Save to database cache
        save_answer(intent, cached_json, db_path="cache.db")

        try:
            # When screenshot is None, ai_engine retrieves answer from database cache
            result = engine.process_screen_and_intent(raw_screenshot=None, user_intent=intent)
            self.assertEqual(result.get("action"), "click")
            self.assertEqual(result.get("text"), "Playing")
        finally:
            if os.path.exists("cache.db"):
                os.remove("cache.db")


if __name__ == "__main__":
    unittest.main()
