import os
import sqlite3
import tempfile
import unittest
from database import get_cached_answer, save_answer, init_db


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")
        os.close(self.db_fd)
        init_db(self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_save_and_get_cached_answer(self):
        intent = "Ouvrir le navigateur"
        answer = '{"action": "click", "x": 100, "y": 200}'

        self.assertIsNone(get_cached_answer(intent, db_path=self.db_path))

        save_answer(intent, answer, db_path=self.db_path)
        cached = get_cached_answer(intent, db_path=self.db_path)

        self.assertEqual(cached, answer)

    def test_update_cached_answer(self):
        intent = "Ouvrir la musique"
        answer_v1 = '{"action": "wait"}'
        answer_v2 = '{"action": "click", "x": 50, "y": 50}'

        save_answer(intent, answer_v1, db_path=self.db_path)
        save_answer(intent, answer_v2, db_path=self.db_path)

        cached = get_cached_answer(intent, db_path=self.db_path)
        self.assertEqual(cached, answer_v2)

    def test_sql_injection_prevention(self):
        # Payload trying to perform SQL injection and drop the table
        sql_injection_payload = "test' OR '1'='1'; DROP TABLE answer_cache; --"
        answer = '{"action": "none", "text": "safe"}'

        # Save using payload as user_intent
        save_answer(sql_injection_payload, answer, db_path=self.db_path)

        # Retrieve using exact payload
        cached = get_cached_answer(sql_injection_payload, db_path=self.db_path)
        self.assertEqual(cached, answer)

        # Confirm the table answer_cache still exists and was not dropped
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='answer_cache';")
            self.assertIsNotNone(cursor.fetchone())


if __name__ == "__main__":
    unittest.main()
