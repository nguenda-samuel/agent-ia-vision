import os
import sqlite3
import tempfile
import unittest

from database import _ensure_db_init, get_cached_answer, save_answer


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_save_and_get_cached_answer(self):
        intent = "Open music player"
        response = '{"action": "click", "x": 100, "y": 200, "text": "Playing music"}'

        save_answer(intent, response, db_path=self.db_path)
        cached = get_cached_answer(intent, db_path=self.db_path)

        self.assertEqual(cached, response)

    def test_update_existing_cache(self):
        intent = "Open music player"
        response_v1 = '{"action": "wait", "text": "Loading"}'
        response_v2 = '{"action": "click", "text": "Ready"}'

        save_answer(intent, response_v1, db_path=self.db_path)
        save_answer(intent, response_v2, db_path=self.db_path)

        cached = get_cached_answer(intent, db_path=self.db_path)
        self.assertEqual(cached, response_v2)

    def test_sql_injection_protection(self):
        sql_injection_payload = "' OR '1'='1'; DROP TABLE answer_cache; --"
        fake_response = '{"action": "none", "text": "Hacked"}'

        save_answer(sql_injection_payload, fake_response, db_path=self.db_path)

        # Ensure the table still exists and query works
        cached = get_cached_answer(sql_injection_payload, db_path=self.db_path)
        self.assertEqual(cached, fake_response)

        # Verify a normal query doesn't match the payload
        self.assertIsNone(get_cached_answer("normal query", db_path=self.db_path))

        # Verify table structure remains intact in the database
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='answer_cache'"
            )
            self.assertIsNotNone(cursor.fetchone())


if __name__ == "__main__":
    unittest.main()
