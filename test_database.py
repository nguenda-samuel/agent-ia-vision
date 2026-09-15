import os
import unittest
from database import _init_db, get_cached_answer, save_answer

TEST_DB = "test_cache.db"


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)
        _init_db(TEST_DB)

    def tearDown(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_save_and_get_cached_answer(self):
        save_answer(
            "Open browser",
            '{"action": "click", "x": 100, "y": 200}',
            db_path=TEST_DB,
        )
        res = get_cached_answer("Open browser", db_path=TEST_DB)
        self.assertEqual(res, '{"action": "click", "x": 100, "y": 200}')

    def test_get_nonexistent_answer(self):
        res = get_cached_answer("Nonexistent query", db_path=TEST_DB)
        self.assertIsNone(res)

    def test_sql_injection_prevention(self):
        sqli_payload = "test' OR '1'='1"
        save_answer(sqli_payload, '{"action": "none"}', db_path=TEST_DB)

        # Searching for normal intent should NOT match sqli_payload
        self.assertIsNone(get_cached_answer("normal query", db_path=TEST_DB))
        # Searching for exact string should work safely
        self.assertEqual(
            get_cached_answer(sqli_payload, db_path=TEST_DB),
            '{"action": "none"}',
        )


if __name__ == "__main__":
    unittest.main()
