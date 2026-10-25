import os
import sqlite3
import tempfile
import unittest

from database import get_cached_answer, save_answer


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")
        os.close(self.db_fd)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)

    def test_get_cached_answer_empty(self):
        result = get_cached_answer("Open Chrome", db_path=self.db_path)
        self.assertIsNone(result)

    def test_save_and_get_cached_answer(self):
        user_intent = "Open Settings"
        response = '{"action": "click", "x": 100, "y": 200, "text": "Opening settings"}'

        save_answer(user_intent, response, db_path=self.db_path)
        cached = get_cached_answer(user_intent, db_path=self.db_path)

        self.assertEqual(cached, response)

    def test_update_existing_cache(self):
        user_intent = "Open Settings"
        initial_response = '{"action": "click", "x": 100, "y": 200}'
        updated_response = '{"action": "click", "x": 150, "y": 250}'

        save_answer(user_intent, initial_response, db_path=self.db_path)
        save_answer(user_intent, updated_response, db_path=self.db_path)

        cached = get_cached_answer(user_intent, db_path=self.db_path)
        self.assertEqual(cached, updated_response)

    def test_sql_injection_prevention_get(self):
        sqli_payload = "'; DROP TABLE answer_cache; --"
        save_answer("legit_intent", "legit_response", db_path=self.db_path)

        result = get_cached_answer(sqli_payload, db_path=self.db_path)
        self.assertIsNone(result)

        # Confirm table still exists and data intact
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT cached_response FROM answer_cache WHERE user_intent = ?", ("legit_intent",))
            row = cursor.fetchone()
            self.assertIsNotNone(row)
            self.assertEqual(row[0], "legit_response")

    def test_sql_injection_prevention_save(self):
        sqli_payload = "' OR '1'='1"
        sqli_response = "injected_response"

        save_answer(sqli_payload, sqli_response, db_path=self.db_path)

        cached = get_cached_answer(sqli_payload, db_path=self.db_path)
        self.assertEqual(cached, sqli_response)

        # Ensure other queries are not matched
        self.assertIsNone(get_cached_answer("other_intent", db_path=self.db_path))


if __name__ == "__main__":
    unittest.main()
