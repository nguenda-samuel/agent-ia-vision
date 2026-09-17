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
        user_intent = "What is the capital of France?"
        answer = '{"action": "none", "text": "Paris"}'

        save_answer(user_intent, answer, db_path=TEST_DB)
        cached = get_cached_answer(user_intent, db_path=TEST_DB)

        self.assertEqual(cached, answer)

    def test_sql_injection_prevention(self):
        sqli_intent = "test' OR '1'='1"
        answer = '{"action": "none", "text": "Safe response"}'

        save_answer(sqli_intent, answer, db_path=TEST_DB)

        # Non-existent intent should return None, not match all records due to SQLi
        cached_other = get_cached_answer("another intent", db_path=TEST_DB)
        self.assertIsNone(cached_other)

        # Exact match should return answer
        cached = get_cached_answer(sqli_intent, db_path=TEST_DB)
        self.assertEqual(cached, answer)


if __name__ == "__main__":
    unittest.main()
