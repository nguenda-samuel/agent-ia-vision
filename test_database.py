import os
import tempfile
import unittest
from database import get_cached_answer, save_answer, _init_db


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")
        _init_db(self.db_path)

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_save_and_get_cached_answer(self):
        user_intent = "Ouvre le navigateur"
        answer = '{"action": "click", "x": 100, "y": 200, "text": "Ouverture"}'

        save_answer(user_intent, answer, db_path=self.db_path)
        cached = get_cached_answer(user_intent, db_path=self.db_path)

        self.assertEqual(cached, answer)

    def test_get_nonexistent_cached_answer(self):
        cached = get_cached_answer("Commande inconnue", db_path=self.db_path)
        self.assertIsNone(cached)

    def test_update_existing_cached_answer(self):
        user_intent = "Joue de la musique"
        answer1 = "Reponse 1"
        answer2 = "Reponse 2"

        save_answer(user_intent, answer1, db_path=self.db_path)
        save_answer(user_intent, answer2, db_path=self.db_path)

        cached = get_cached_answer(user_intent, db_path=self.db_path)
        self.assertEqual(cached, answer2)

    def test_sql_injection_protection(self):
        # Payload trying SQL injection via single quotes, OR conditions, and DROP TABLE commands
        sqli_payloads = [
            "' OR '1'='1",
            "'; DROP TABLE answers_cache; --",
            "SELECT * FROM answers_cache WHERE 'a'='a",
            'user" OR "1"="1',
        ]

        for payload in sqli_payloads:
            answer = f"Safe response for {payload}"
            # Test that saving payload doesn't raise SQL syntax error or drop tables
            save_answer(payload, answer, db_path=self.db_path)

            # Test that querying payload retrieves exact string safely
            cached = get_cached_answer(payload, db_path=self.db_path)
            self.assertEqual(cached, answer)

        # Confirm the table still exists and functions normally after SQL injection attempts
        test_intent = "Valid intent"
        save_answer(test_intent, "Valid response", db_path=self.db_path)
        self.assertEqual(get_cached_answer(test_intent, db_path=self.db_path), "Valid response")


if __name__ == "__main__":
    unittest.main()
