import os
import tempfile
import unittest

from database import get_cached_answer, save_answer


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.db_path = self.temp_db.name
        self.temp_db.close()

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_save_and_get_cached_answer(self):
        prompt = "Open Youtube"
        answer = '{"action": "click", "x": 100, "y": 200, "text": "Opening Youtube"}'

        self.assertIsNone(get_cached_answer(prompt, db_path=self.db_path))

        save_answer(prompt, answer, db_path=self.db_path)

        cached = get_cached_answer(prompt, db_path=self.db_path)
        self.assertEqual(cached, answer)

    def test_sql_injection_safety(self):
        malicious_prompt = "' OR '1'='1"
        answer = '{"action": "none", "text": "safe response"}'

        save_answer(malicious_prompt, answer, db_path=self.db_path)

        # Ensure that retrieving with exact malicious string works and does not leak or alter query logic
        cached = get_cached_answer(malicious_prompt, db_path=self.db_path)
        self.assertEqual(cached, answer)

        # Ensure that a different prompt returns None (injection didn't match all rows)
        self.assertIsNone(get_cached_answer("normal prompt", db_path=self.db_path))


if __name__ == "__main__":
    unittest.main()
