import os
import sqlite3
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
        intent = "Ouvrir le navigateur"
        answer = '{"action": "click", "x": 100, "y": 200, "text": "Clic sur Chrome"}'

        save_answer(intent, answer, db_path=self.db_path)
        cached = get_cached_answer(intent, db_path=self.db_path)

        self.assertEqual(cached, answer)

    def test_update_existing_cache(self):
        intent = "Fermer la fenêtre"
        answer1 = '{"action": "click", "x": 10, "y": 10}'
        answer2 = '{"action": "click", "x": 20, "y": 20}'

        save_answer(intent, answer1, db_path=self.db_path)
        save_answer(intent, answer2, db_path=self.db_path)

        cached = get_cached_answer(intent, db_path=self.db_path)
        self.assertEqual(cached, answer2)

    def test_sql_injection_resilience(self):
        # SQL Injection attempt in user_intent
        malicious_intent = "test' OR '1'='1"
        answer = '{"action": "none"}'

        save_answer(malicious_intent, answer, db_path=self.db_path)

        # Ensure searching for another intent does not return the malicious intent's answer
        other = get_cached_answer("normal_intent", db_path=self.db_path)
        self.assertIsNone(other)

        # Ensure exact lookup matches safely without executing injection
        retrieved = get_cached_answer(malicious_intent, db_path=self.db_path)
        self.assertEqual(retrieved, answer)

        # SQL Injection drop table attempt
        drop_attempt = "'; DROP TABLE qa_cache; --"
        save_answer(drop_attempt, answer, db_path=self.db_path)

        # Verify table was not dropped and data intact
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='qa_cache'"
            )
            self.assertIsNotNone(cursor.fetchone())

    def test_empty_or_none_inputs(self):
        self.assertIsNone(get_cached_answer("", db_path=self.db_path))
        self.assertIsNone(get_cached_answer(None, db_path=self.db_path))

        save_answer("", "answer", db_path=self.db_path)
        save_answer("intent", None, db_path=self.db_path)
        self.assertIsNone(get_cached_answer("intent", db_path=self.db_path))


if __name__ == "__main__":
    unittest.main()
