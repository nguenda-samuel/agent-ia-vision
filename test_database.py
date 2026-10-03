import os
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
        intent = "Open settings"
        response = '{"action": "click", "x": 10, "y": 20}'

        self.assertIsNone(get_cached_answer(intent, db_path=self.db_path))

        save_answer(intent, response, db_path=self.db_path)

        cached = get_cached_answer(intent, db_path=self.db_path)
        self.assertEqual(cached, response)

    def test_sql_injection_prevention(self):
        sqli_payload = "' OR '1'='1"
        response = '{"action": "none", "text": "safe"}'

        save_answer(sqli_payload, response, db_path=self.db_path)

        # Retrieval with exact string should work
        cached = get_cached_answer(sqli_payload, db_path=self.db_path)
        self.assertEqual(cached, response)

        # Non-matching intent should return None, not match all records due to SQL injection
        self.assertIsNone(
            get_cached_answer("another_intent", db_path=self.db_path)
        )


if __name__ == "__main__":
    unittest.main()
