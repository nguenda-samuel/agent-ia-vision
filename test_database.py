import os
import tempfile
import unittest

from database import get_cached_answer, save_answer


class TestDatabaseSecurity(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_save_and_get_cached_answer(self):
        intent = "Open Settings"
        response = '{"action": "none", "text": "Opening settings"}'

        save_answer(intent, response, db_path=self.db_path)
        cached = get_cached_answer(intent, db_path=self.db_path)

        self.assertEqual(cached, response)

    def test_sql_injection_safety(self):
        sqli_payload = "test' OR '1'='1"
        response = '{"action": "none", "text": "Safe response"}'

        save_answer(sqli_payload, response, db_path=self.db_path)

        # Ensure searching for non-matching intent returns None, not all rows
        result = get_cached_answer("non_existent_intent", db_path=self.db_path)
        self.assertIsNone(result)

        # Searching for exact payload returns saved response
        result_payload = get_cached_answer(sqli_payload, db_path=self.db_path)
        self.assertEqual(result_payload, response)


if __name__ == "__main__":
    unittest.main()
