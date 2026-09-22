import os
import sqlite3
import tempfile
import unittest
from database import get_cached_answer, save_answer


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.db_path = self.temp_db.name
        self.temp_db.close()

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_save_and_get_cached_answer(self):
        intent = "ouvre google"
        response = '{"action": "click", "x": 100, "y": 200, "text": "Ouverture"}'

        self.assertIsNone(get_cached_answer(intent, db_path=self.db_path))

        save_answer(intent, response, db_path=self.db_path)

        cached = get_cached_answer(intent, db_path=self.db_path)
        self.assertEqual(cached, response)

    def test_update_cached_answer(self):
        intent = "ouvre google"
        response1 = '{"action": "none", "text": "1"}'
        response2 = '{"action": "none", "text": "2"}'

        save_answer(intent, response1, db_path=self.db_path)
        self.assertEqual(get_cached_answer(intent, db_path=self.db_path), response1)

        save_answer(intent, response2, db_path=self.db_path)
        self.assertEqual(get_cached_answer(intent, db_path=self.db_path), response2)

    def test_sql_injection_safety(self):
        sql_injection_payload = "test' OR '1'='1"
        response = '{"action": "none", "text": "Safe"}'

        save_answer(sql_injection_payload, response, db_path=self.db_path)

        # Ensure retrieving with exact payload works safely
        self.assertEqual(get_cached_answer(sql_injection_payload, db_path=self.db_path), response)

        # Ensure that searching for another string does not return the payload's response via SQL injection
        self.assertIsNone(get_cached_answer("another_intent", db_path=self.db_path))


if __name__ == "__main__":
    unittest.main()
