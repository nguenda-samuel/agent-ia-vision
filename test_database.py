import os
import sqlite3
import unittest
from database import get_cached_answer, save_answer, _ensure_db_init

TEST_DB_PATH = "test_cache.db"


class TestDatabaseCacheSecurity(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)
        _ensure_db_init(TEST_DB_PATH)

    def tearDown(self):
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)

    def test_save_and_get_cached_answer(self):
        save_answer("Click on submit", '{"action": "click"}', db_path=TEST_DB_PATH)
        result = get_cached_answer("Click on submit", db_path=TEST_DB_PATH)
        self.assertEqual(result, '{"action": "click"}')

    def test_get_nonexistent_answer(self):
        result = get_cached_answer("Unknown intent", db_path=TEST_DB_PATH)
        self.assertIsNone(result)

    def test_update_existing_answer(self):
        save_answer("Open menu", '{"action": "click", "x": 10}', db_path=TEST_DB_PATH)
        save_answer("Open menu", '{"action": "click", "x": 20}', db_path=TEST_DB_PATH)
        result = get_cached_answer("Open menu", db_path=TEST_DB_PATH)
        self.assertEqual(result, '{"action": "click", "x": 20}')

    def test_sql_injection_prevention_in_get_and_save(self):
        sqli_payload = "test' OR '1'='1"
        save_answer(sqli_payload, '{"action": "none"}', db_path=TEST_DB_PATH)

        # Ensure exact match is retrieved and non-matching query returns None
        self.assertEqual(get_cached_answer(sqli_payload, db_path=TEST_DB_PATH), '{"action": "none"}')
        self.assertIsNone(get_cached_answer("other intent", db_path=TEST_DB_PATH))

        # Attempt table drop attack payload
        drop_payload = "intent'; DROP TABLE answer_cache; --"
        save_answer(drop_payload, '{"action": "drop"}', db_path=TEST_DB_PATH)
        self.assertEqual(get_cached_answer(drop_payload, db_path=TEST_DB_PATH), '{"action": "drop"}')

        # Verify table still exists and operates normally
        with sqlite3.connect(TEST_DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT count(*) FROM answer_cache")
            count = cursor.fetchone()[0]
            self.assertEqual(count, 2)


if __name__ == "__main__":
    unittest.main()
