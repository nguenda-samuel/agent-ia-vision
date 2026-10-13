import os
import tempfile
import unittest
import database


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_save_and_get_cached_answer(self):
        intent = "test_intent"
        answer = '{"action": "none", "text": "Hello world"}'

        self.assertIsNone(database.get_cached_answer(intent, db_path=self.db_path))

        database.save_answer(intent, answer, db_path=self.db_path)
        cached = database.get_cached_answer(intent, db_path=self.db_path)

        self.assertEqual(cached, answer)

    def test_sql_injection_safety(self):
        # Malicious string designed to trigger SQL injection if string formatted
        malicious_intent = "test'; DROP TABLE cached_answers; --"
        answer = '{"action": "safe"}'

        database.save_answer(malicious_intent, answer, db_path=self.db_path)
        cached = database.get_cached_answer(malicious_intent, db_path=self.db_path)

        self.assertEqual(cached, answer)


if __name__ == "__main__":
    unittest.main()
