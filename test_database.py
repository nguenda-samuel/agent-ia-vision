import os
import tempfile
import unittest

from database import get_cached_answer, save_answer


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        self.db_file = tempfile.NamedTemporaryFile(delete=False)
        self.db_path = self.db_file.name
        self.db_file.close()

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_save_and_get_cached_answer(self):
        intent = "ouvrir le navigateur"
        response = '{"action": "click", "x": 100, "y": 200, "text": "Ouverture"}'

        save_answer(intent, response, db_path=self.db_path)
        cached = get_cached_answer(intent, db_path=self.db_path)

        self.assertEqual(cached, response)

    def test_get_nonexistent_cached_answer(self):
        cached = get_cached_answer("intent_inconnu", db_path=self.db_path)
        self.assertIsNone(cached)

    def test_update_cached_answer(self):
        intent = "cliquer"
        res1 = "reponse 1"
        res2 = "reponse 2"

        save_answer(intent, res1, db_path=self.db_path)
        save_answer(intent, res2, db_path=self.db_path)

        cached = get_cached_answer(intent, db_path=self.db_path)
        self.assertEqual(cached, res2)

    def test_sql_injection_prevention(self):
        malicious_intent = "test'; DROP TABLE answer_cache; --"
        response = "safe_response"

        save_answer(malicious_intent, response, db_path=self.db_path)
        cached = get_cached_answer(malicious_intent, db_path=self.db_path)

        self.assertEqual(cached, response)

        # Confirm table still exists and normal query works
        normal_intent = "normal_intent"
        save_answer(normal_intent, "normal_response", db_path=self.db_path)
        self.assertEqual(
            get_cached_answer(normal_intent, db_path=self.db_path),
            "normal_response",
        )


if __name__ == "__main__":
    unittest.main()
