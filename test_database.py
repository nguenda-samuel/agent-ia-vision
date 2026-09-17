import os
import sqlite3
import tempfile
import unittest

from database import get_cached_answer, save_answer


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_save_and_get_cached_answer(self):
        intent = "test_intent"
        response = "cached_test_response"

        self.assertIsNone(get_cached_answer(intent, db_path=self.db_path))

        save_answer(intent, response, db_path=self.db_path)
        self.assertEqual(
            get_cached_answer(intent, db_path=self.db_path), response
        )

    def test_update_cached_answer(self):
        intent = "test_intent"
        response1 = "response_1"
        response2 = "response_2"

        save_answer(intent, response1, db_path=self.db_path)
        self.assertEqual(
            get_cached_answer(intent, db_path=self.db_path), response1
        )

        save_answer(intent, response2, db_path=self.db_path)
        self.assertEqual(
            get_cached_answer(intent, db_path=self.db_path), response2
        )

    def test_sql_injection_prevention(self):
        sql_injection_intent = "' OR '1'='1"
        response = "safe_response"

        save_answer(sql_injection_intent, response, db_path=self.db_path)

        cached = get_cached_answer(sql_injection_intent, db_path=self.db_path)
        self.assertEqual(cached, response)

        # Ensure normal queries don't match or execute arbitrary SQL
        other_intent = "other_intent"
        self.assertIsNone(get_cached_answer(other_intent, db_path=self.db_path))


if __name__ == "__main__":
    unittest.main()
