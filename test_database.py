import os
import sqlite3
import tempfile
import unittest

from database import get_cached_answer, save_answer


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_save_and_get_cached_answer(self):
        intent = "Open browser"
        answer = '{"action": "click", "x": 100, "y": 200, "text": "Opening browser"}'

        save_answer(intent, answer, db_path=self.db_path)
        cached = get_cached_answer(intent, db_path=self.db_path)

        self.assertEqual(cached, answer)

    def test_sql_injection_prevention(self):
        sqli_intent = "test' OR '1'='1"
        save_answer(sqli_intent, "safe_answer", db_path=self.db_path)

        # Non-matching query should return None rather than executing injection
        self.assertIsNone(
            get_cached_answer("non_existent_intent", db_path=self.db_path)
        )
        # Querying exact injected string should safely return saved answer
        self.assertEqual(
            get_cached_answer(sqli_intent, db_path=self.db_path), "safe_answer"
        )


if __name__ == "__main__":
    unittest.main()
