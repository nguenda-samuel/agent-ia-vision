import os
import tempfile
import unittest

from database import get_cached_answer, init_db, save_answer


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")
        os.close(self.db_fd)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_save_and_get_cached_answer(self):
        intent = "Ouvre le navigateur"
        response = '{"action": "click", "x": 100, "y": 200, "text": "Ouverture du navigateur"}'
        save_answer(intent, response, db_path=self.db_path)

        cached = get_cached_answer(intent, db_path=self.db_path)
        self.assertEqual(cached, response)

    def test_update_cached_answer(self):
        intent = "Ouvre le navigateur"
        response1 = '{"action": "wait", "text": "Chargement"}'
        response2 = '{"action": "none", "text": "Prêt"}'

        save_answer(intent, response1, db_path=self.db_path)
        save_answer(intent, response2, db_path=self.db_path)

        cached = get_cached_answer(intent, db_path=self.db_path)
        self.assertEqual(cached, response2)

    def test_get_cached_answer_not_found(self):
        cached = get_cached_answer("Intent inconnu", db_path=self.db_path)
        self.assertIsNone(cached)

    def test_sql_injection_resistance(self):
        # Intent malicious containing SQL injection payload
        malicious_intent = "test' OR '1'='1' --"
        malicious_response = "secret response"

        save_answer(malicious_intent, malicious_response, db_path=self.db_path)

        # Ensure that searching for another string does NOT match via SQL injection
        other_cached = get_cached_answer("another_intent", db_path=self.db_path)
        self.assertIsNone(other_cached)

        # Ensure the exact string intent returns the correct stored value safely
        exact_cached = get_cached_answer(malicious_intent, db_path=self.db_path)
        self.assertEqual(exact_cached, malicious_response)

        # Attempt DROP TABLE payload as intent
        drop_intent = "'; DROP TABLE answer_cache; --"
        save_answer(drop_intent, "drop_response", db_path=self.db_path)
        # Ensure table still exists and query succeeds
        self.assertEqual(
            get_cached_answer(drop_intent, db_path=self.db_path), "drop_response"
        )


if __name__ == "__main__":
    unittest.main()
