import os
import sqlite3
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
        intent = "ouvrir le navigateur"
        response = '{"action": "click", "x": 100, "y": 200, "text": "Ouverture"}'

        save_answer(intent, response, db_path=self.path_str())
        cached = get_cached_answer(intent, db_path=self.path_str())

        self.assertEqual(cached, response)

    def test_get_nonexistent_cached_answer(self):
        cached = get_cached_answer("intent_inconnue", db_path=self.path_str())
        self.assertIsNone(cached)

    def test_update_cached_answer(self):
        intent = "ouvrir le navigateur"
        response1 = '{"action": "wait"}'
        response2 = '{"action": "click"}'

        save_answer(intent, response1, db_path=self.path_str())
        save_answer(intent, response2, db_path=self.path_str())

        cached = get_cached_answer(intent, db_path=self.path_str())
        self.assertEqual(cached, response2)

    def test_sql_injection_prevention(self):
        # Payload SQL injection essayant de dropper la table ou contourner la clause WHERE
        malicious_intent = "'; DROP TABLE cache; --"
        malicious_response = '{"action": "none"}'

        save_answer(malicious_intent, malicious_response, db_path=self.path_str())
        cached = get_cached_answer(malicious_intent, db_path=self.path_str())

        # Vérifie que la chaîne malicieuse a été traitée comme une simple donnée texte
        self.assertEqual(cached, malicious_response)

        # Vérifie que la table cache existe toujours
        with sqlite3.connect(self.path_str()) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT count(*) FROM cache")
            count = cursor.fetchone()[0]
            self.assertEqual(count, 1)

    def test_sql_injection_quote_handling(self):
        intent_with_quotes = "O'Connor's test OR 1=1 --"
        response = "safe response"

        save_answer(intent_with_quotes, response, db_path=self.path_str())
        cached = get_cached_answer(intent_with_quotes, db_path=self.path_str())

        self.assertEqual(cached, response)

    def path_str(self):
        return self.db_path


if __name__ == "__main__":
    unittest.main()
