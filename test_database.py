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
        intent = "test intent"
        response = '{"action": "none", "text": "hello"}'

        self.assertIsNone(get_cached_answer(intent, db_path=self.db_path))

        save_answer(intent, response, db_path=self.db_path)

        cached = get_cached_answer(intent, db_path=self.db_path)
        self.assertEqual(cached, response)

    def test_update_cached_answer(self):
        intent = "test intent"
        response1 = '{"action": "none", "text": "first"}'
        response2 = '{"action": "none", "text": "updated"}'

        save_answer(intent, response1, db_path=self.db_path)
        self.assertEqual(get_cached_answer(intent, db_path=self.db_path), response1)

        save_answer(intent, response2, db_path=self.db_path)
        self.assertEqual(get_cached_answer(intent, db_path=self.db_path), response2)

    def test_sql_injection_prevention(self):
        # Attempt SQL injection in intent payload
        sqli_intent = "test' OR '1'='1"
        sqli_response = '{"action": "none", "text": "injection test"}'

        save_answer(sqli_intent, sqli_response, db_path=self.db_path)

        # Ensure literal match works and doesn't return unintended data
        self.assertEqual(get_cached_answer(sqli_intent, db_path=self.db_path), sqli_response)
        self.assertIsNone(get_cached_answer("test", db_path=self.db_path))


if __name__ == "__main__":
    unittest.main()
