import os
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
        prompt = "How to open settings?"
        answer = '{"action": "click", "x": 100, "y": 200, "text": "Clicking settings"}'

        save_answer(prompt, answer, db_path=self.db_path)
        cached = get_cached_answer(prompt, db_path=self.db_path)

        self.assertEqual(cached, answer)

    def test_get_nonexistent_prompt(self):
        cached = get_cached_answer("Nonexistent prompt", db_path=self.db_path)
        self.assertIsNone(cached)

    def test_sql_injection_prevention(self):
        # Payload attempting SQL injection
        sqli_prompt = "test' OR '1'='1"
        sqli_answer = "malicious payload"

        save_answer(sqli_prompt, sqli_answer, db_path=self.db_path)

        # Retrieving standard prompt should return None, not sqli_answer
        normal_cached = get_cached_answer("normal prompt", db_path=self.db_path)
        self.assertIsNone(normal_cached)

        # Retrieving exact sqli_prompt returns exact match securely
        cached = get_cached_answer(sqli_prompt, db_path=self.db_path)
        self.assertEqual(cached, sqli_answer)


if __name__ == "__main__":
    unittest.main()
