import os
import sqlite3
import tempfile
import unittest

from database import get_cached_answer, save_answer


class TestDatabaseCacheSecurity(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_save_and_get_cached_answer(self):
        user_intent = "Open settings menu"
        response = '{"action": "click", "x": 100, "y": 200}'

        save_answer(user_intent, response, db_path=self.db_path)
        cached = get_cached_answer(user_intent, db_path=self.db_path)

        self.assertEqual(cached, response)

    def test_sql_injection_prevention_get(self):
        # Insert legitimate answer
        save_answer("normal_intent", "normal_response", db_path=self.db_path)

        # Attempt SQL injection attack payload
        sqli_intent = "' OR '1'='1"
        result = get_cached_answer(sqli_intent, db_path=self.db_path)

        # Should return None because payload is treated as a literal string value
        self.assertIsNone(result)

    def test_sql_injection_prevention_save(self):
        sqli_intent = "intent'; DROP TABLE answer_cache; --"
        sqli_response = "malicious_response"

        # Save should safely insert the string without executing the dropped table command
        save_answer(sqli_intent, sqli_response, db_path=self.db_path)

        # Verify table still exists and record can be retrieved as literal
        result = get_cached_answer(sqli_intent, db_path=self.db_path)
        self.assertEqual(result, sqli_response)

        # Confirm answer_cache table was not dropped
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='answer_cache';")
            self.assertIsNotNone(cursor.fetchone())


if __name__ == "__main__":
    unittest.main()
