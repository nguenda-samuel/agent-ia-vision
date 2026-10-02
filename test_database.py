import os
import sqlite3
import unittest
import database


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        self.test_db = "test_cache.db"
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_save_and_get_cached_answer(self):
        intent = "Open browser"
        response = '{"action": "click", "x": 100, "y": 200, "text": "Opening browser"}'

        # Cache should initially be empty
        self.assertIsNone(database.get_cached_answer(intent, db_path=self.test_db))

        # Save answer
        database.save_answer(intent, response, db_path=self.test_db)

        # Retrieve cached answer
        cached = database.get_cached_answer(intent, db_path=self.test_db)
        self.assertEqual(cached, response)

    def test_sql_injection_prevention(self):
        # SQL injection attempt payload in user_intent
        sqli_payload = "'; DROP TABLE answer_cache; --"
        response = "Safe response"

        database.save_answer(sqli_payload, response, db_path=self.test_db)

        # Verify payload was treated as literal string and answer cache table still exists
        cached = database.get_cached_answer(sqli_payload, db_path=self.test_db)
        self.assertEqual(cached, response)

        # Verify table structure is intact
        with sqlite3.connect(self.test_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='answer_cache'")
            self.assertIsNotNone(cursor.fetchone())


if __name__ == "__main__":
    unittest.main()
