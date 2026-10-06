import os
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
        intent = "Open browser"
        response = '{"action": "click", "x": 100, "y": 200, "text": "Opening browser"}'

        self.assertIsNone(get_cached_answer(intent, db_path=TEST_DB))

        save_answer(intent, response, db_path=TEST_DB)

        cached = get_cached_answer(intent, db_path=TEST_DB)
        self.assertEqual(cached, response)

    def test_update_cached_answer(self):
        intent = "Open browser"
        response1 = "Old response"
        response2 = "New response"

        save_answer(intent, response1, db_path=TEST_DB)
        self.assertEqual(get_cached_answer(intent, db_path=TEST_DB), response1)

        save_answer(intent, response2, db_path=TEST_DB)
        self.assertEqual(get_cached_answer(intent, db_path=TEST_DB), response2)

    def test_sql_injection_prevention(self):
        sqli_intent = "' OR '1'='1"
        response = "Secret or fake payload"

        save_answer(sqli_intent, response, db_path=TEST_DB)

        # Retrieving exact intent works securely without affecting other rows
        self.assertEqual(get_cached_answer(sqli_intent, db_path=TEST_DB), response)
        # Attempting query with standard non-existent intent returns None
        self.assertIsNone(get_cached_answer("normal_intent", db_path=TEST_DB))


if __name__ == "__main__":
    unittest.main()
