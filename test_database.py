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
        save_answer(intent, response, db_path=self.db_path)

        cached = get_cached_answer(intent, db_path=self.db_path)
        self.assertEqual(cached, response)

    def test_sql_injection_prevention(self):
        malicious_intent = "' OR '1'='1"
        response = '{"action": "none", "text": "safe"}'
        save_answer(malicious_intent, response, db_path=self.db_path)

        cached = get_cached_answer(malicious_intent, db_path=self.db_path)
        self.assertEqual(cached, response)

        # Ensure that non-matching intent returns None instead of all rows
        normal_intent = "normal intent"
        cached_normal = get_cached_answer(normal_intent, db_path=self.db_path)
        self.assertIsNone(cached_normal)

    def test_upsert_on_conflict(self):
        intent = "test intent"
        first_response = '{"action": "none", "text": "first"}'
        second_response = '{"action": "none", "text": "second"}'

        save_answer(intent, first_response, db_path=self.db_path)
        save_answer(intent, second_response, db_path=self.db_path)

        cached = get_cached_answer(intent, db_path=self.db_path)
        self.assertEqual(cached, second_response)


if __name__ == "__main__":
    unittest.main()
