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
        intent = "ouvrir le navigateur"
        response = '{"action": "click", "x": 100, "y": 200, "text": "Ouverture"}'

        save_answer(intent, response, db_path=self.db_path)
        cached = get_cached_answer(intent, db_path=self.db_path)

        self.assertEqual(cached, response)

    def test_get_nonexistent_answer(self):
        cached = get_cached_answer("intent non existant", db_path=self.db_path)
        self.assertIsNone(cached)

    def test_sql_injection_prevention(self):
        # Tentative d'injection SQL
        malicious_intent = "test' OR '1'='1"
        malicious_response = '{"action": "none", "text": "pwned"}'

        save_answer(malicious_intent, malicious_response, db_path=self.db_path)

        # Doit retourner None pour un intent non malicieux
        self.assertIsNone(get_cached_answer("test", db_path=self.db_path))

        # Doit retourner exactement la valeur enregistrée sous la clé brute sans exécuter d'injection
        self.assertEqual(
            get_cached_answer(malicious_intent, db_path=self.db_path),
            malicious_response,
        )


if __name__ == "__main__":
    unittest.main()
