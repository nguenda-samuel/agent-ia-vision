import os
import sqlite3
import unittest
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
        user_intent = "Ouvrir le navigateur"
        cached_response = '{"action": "click", "x": 100, "y": 200, "text": "Clic sur le navigateur"}'

        save_answer(user_intent, cached_response, db_path=TEST_DB)
        retrieved = get_cached_answer(user_intent, db_path=TEST_DB)

        self.assertEqual(retrieved, cached_response)

    def test_get_non_existent_answer(self):
        retrieved = get_cached_answer("Intent inconnu", db_path=TEST_DB)
        self.assertIsNone(retrieved)

    def test_update_existing_cached_answer(self):
        user_intent = "Ouvrir le navigateur"
        response1 = '{"action": "none"}'
        response2 = '{"action": "click"}'

        save_answer(user_intent, response1, db_path=TEST_DB)
        save_answer(user_intent, response2, db_path=TEST_DB)

        retrieved = get_cached_answer(user_intent, db_path=TEST_DB)
        self.assertEqual(retrieved, response2)

    def test_sql_injection_prevention(self):
        sqli_intent = "' OR '1'='1"
        sqli_response = "injected_response"

        save_answer(sqli_intent, sqli_response, db_path=TEST_DB)

        # Normal query for sqli_intent should return sqli_response
        self.assertEqual(get_cached_answer(sqli_intent, db_path=TEST_DB), sqli_response)

        # Another intent should still return None and not be affected by SQL injection
        self.assertIsNone(get_cached_answer("Autre intent", db_path=TEST_DB))


if __name__ == "__main__":
    unittest.main()
