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
        user_intent = "Open browser"
        response = '{"action": "click", "x": 100, "y": 200, "text": "Opening browser"}'

        self.assertIsNone(get_cached_answer(user_intent, db_path=TEST_DB))
        save_answer(user_intent, response, db_path=TEST_DB)
        self.assertEqual(get_cached_answer(user_intent, db_path=TEST_DB), response)

    def test_sql_injection_prevention(self):
        sqli_intent = "test' OR '1'='1"
        sqli_response = "malicious_payload"

        save_answer(sqli_intent, sqli_response, db_path=TEST_DB)
        self.assertEqual(get_cached_answer(sqli_intent, db_path=TEST_DB), sqli_response)
        self.assertIsNone(get_cached_answer("normal_intent", db_path=TEST_DB))


if __name__ == "__main__":
    unittest.main()
