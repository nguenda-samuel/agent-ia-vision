import os
import sqlite3
import unittest

import database

TEST_DB_PATH = "test_agent_cache.db"


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)

    def tearDown(self):
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)

    def test_save_and_get_cached_answer(self):
        intent = "open settings"
        response = '{"action": "click", "x": 100, "y": 200, "text": "Opening settings"}'

        database.save_answer(intent, response, db_path=TEST_DB_PATH)
        cached = database.get_cached_answer(intent, db_path=TEST_DB_PATH)

        self.assertEqual(cached, response)

    def test_update_cached_answer(self):
        intent = "open settings"
        initial_response = "initial"
        updated_response = "updated"

        database.save_answer(intent, initial_response, db_path=TEST_DB_PATH)
        database.save_answer(intent, updated_response, db_path=TEST_DB_PATH)

        cached = database.get_cached_answer(intent, db_path=TEST_DB_PATH)
        self.assertEqual(cached, updated_response)

    def test_nonexistent_intent(self):
        cached = database.get_cached_answer("nonexistent", db_path=TEST_DB_PATH)
        self.assertIsNone(cached)

    def test_sql_injection_protection(self):
        # Attempt SQL injection payloads as user_intent
        sqli_intent = "' OR '1'='1"
        response = "safe_response"

        database.save_answer(sqli_intent, response, db_path=TEST_DB_PATH)

        # Verify query for a different intent returns None, not all rows
        self.assertIsNone(database.get_cached_answer("normal_intent", db_path=TEST_DB_PATH))
        # Verify exact match retrieves the response safely
        self.assertEqual(database.get_cached_answer(sqli_intent, db_path=TEST_DB_PATH), response)

        # Drop table attempt payload
        drop_intent = "test'; DROP TABLE cache; --"
        database.save_answer(drop_intent, "drop_test", db_path=TEST_DB_PATH)
        self.assertEqual(database.get_cached_answer(drop_intent, db_path=TEST_DB_PATH), "drop_test")

        # Verify cache table still exists
        with sqlite3.connect(TEST_DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='cache'"
            )
            self.assertIsNotNone(cursor.fetchone())


if __name__ == "__main__":
    unittest.main()
