import os
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

    def test_get_cached_answer_missing(self):
        answer = get_cached_answer("non_existent_intent", db_path=self.db_path)
        self.assertIsNone(answer)

    def test_save_and_get_cached_answer(self):
        intent = "ouvre le navigateur"
        response = '{"action": "click", "x": 100, "y": 200, "text": "Ouverture"}'
        save_answer(intent, response, db_path=self.db_path)

        cached = get_cached_answer(intent, db_path=self.db_path)
        self.assertEqual(cached, response)

    def test_upsert_cached_answer(self):
        intent = "jouer de la musique"
        first_resp = '{"action": "none", "text": "Lecture"}'
        second_resp = '{"action": "none", "text": "Pause"}'

        save_answer(intent, first_resp, db_path=self.db_path)
        save_answer(intent, second_resp, db_path=self.db_path)

        cached = get_cached_answer(intent, db_path=self.db_path)
        self.assertEqual(cached, second_resp)

    def test_sql_injection_safety(self):
        # Attempt SQL injection attack in user_intent
        malicious_intent = "test' OR '1'='1"
        response = "safe_response"

        save_answer(malicious_intent, response, db_path=self.db_path)

        # Ensure that non-matching query doesn't return the record
        other = get_cached_answer("other_intent", db_path=self.db_path)
        self.assertIsNone(other)

        # Ensure exact match returns the response safely
        cached = get_cached_answer(malicious_intent, db_path=self.db_path)
        self.assertEqual(cached, response)


if __name__ == "__main__":
    unittest.main()
