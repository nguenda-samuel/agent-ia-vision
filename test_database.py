import os
import unittest
from database import get_cached_answer, save_answer, init_db

TEST_DB = "test_cache.db"


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)
        init_db(TEST_DB)

    def tearDown(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_save_and_get_cached_answer(self):
        intent = "Open Settings"
        answer = '{"action": "click", "x": 100, "y": 200, "text": "Opening settings"}'

        self.assertIsNone(get_cached_answer(intent, db_path=TEST_DB))
        save_answer(intent, answer, db_path=TEST_DB)
        cached = get_cached_answer(intent, db_path=TEST_DB)
        self.assertEqual(cached, answer)

    def test_sql_injection_safety(self):
        intent = "test' OR '1'='1"
        answer = "safe answer"
        save_answer(intent, answer, db_path=TEST_DB)
        self.assertEqual(get_cached_answer(intent, db_path=TEST_DB), answer)
        self.assertIsNone(get_cached_answer("test", db_path=TEST_DB))


if __name__ == "__main__":
    unittest.main()
