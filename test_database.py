import os
import sqlite3
import tempfile
import unittest

from database import get_cached_answer, save_answer


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_get_and_save_answer(self):
        intent = "quelle heure est-il?"
        response = '{"action": "none", "text": "Il est 12h00."}'

        self.assertIsNone(get_cached_answer(intent, db_path=self.db_path))

        save_answer(intent, response, db_path=self.db_path)

        cached = get_cached_answer(intent, db_path=self.db_path)
        self.assertEqual(cached, response)

    def test_save_answer_update_conflict(self):
        intent = "ouvre le navigateur"
        response1 = '{"action": "click", "x": 100, "y": 200}'
        response2 = '{"action": "click", "x": 150, "y": 250}'

        save_answer(intent, response1, db_path=self.db_path)
        self.assertEqual(get_cached_answer(intent, db_path=self.db_path), response1)

        save_answer(intent, response2, db_path=self.db_path)
        self.assertEqual(get_cached_answer(intent, db_path=self.db_path), response2)

    def test_sql_injection_prevention(self):
        injection_intent = "' OR '1'='1' --"
        response = '{"action": "none", "text": "test"}'

        save_answer(injection_intent, response, db_path=self.db_path)

        self.assertEqual(
            get_cached_answer(injection_intent, db_path=self.db_path), response
        )
        self.assertIsNone(
            get_cached_answer("non_existent_intent", db_path=self.db_path)
        )


if __name__ == "__main__":
    unittest.main()
