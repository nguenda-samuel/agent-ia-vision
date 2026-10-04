import os
import unittest
from database import get_cached_answer, save_answer

TEST_DB_PATH = "test_cache.db"


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)

    def tearDown(self):
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)

    def test_save_and_get_cached_answer(self):
        intent = "Open settings"
        answer = '{"action": "click", "x": 100, "y": 200, "text": "Opening settings"}'

        save_answer(intent, answer, db_path=TEST_DB_PATH)
        cached = get_cached_answer(intent, db_path=TEST_DB_PATH)

        self.assertEqual(cached, answer)

    def test_cache_miss_returns_none(self):
        cached = get_cached_answer("Non-existent intent", db_path=TEST_DB_PATH)
        self.assertIsNone(cached)

    def test_sql_injection_safety(self):
        sqli_intent = "test' OR '1'='1"
        answer = '{"action": "none", "text": "Safe"}'

        save_answer(sqli_intent, answer, db_path=TEST_DB_PATH)
        cached = get_cached_answer(sqli_intent, db_path=TEST_DB_PATH)
        self.assertEqual(cached, answer)

        # Ensure SQL injection attempt does not return results for other queries
        other_cached = get_cached_answer("other intent", db_path=TEST_DB_PATH)
        self.assertIsNone(other_cached)


if __name__ == "__main__":
    unittest.main()
