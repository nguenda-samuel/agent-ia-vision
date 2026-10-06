import os
import tempfile
import unittest
from database import get_cached_answer, save_answer


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_db.close()
        self.db_path = self.temp_db.name

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_save_and_get_cached_answer(self):
        intent = "ouvrir le navigateur"
        response = '{"action": "click", "x": 100, "y": 200, "text": "Ouverture"}'

        save_answer(intent, response, db_path=self.db_path)
        cached = get_cached_answer(intent, db_path=self.db_path)

        self.assertEqual(cached, response)

    def test_update_existing_cached_answer(self):
        intent = "fermer la fenêtre"
        response1 = '{"action": "none", "text": "Premier essai"}'
        response2 = '{"action": "none", "text": "Deuxième essai"}'

        save_answer(intent, response1, db_path=self.db_path)
        save_answer(intent, response2, db_path=self.db_path)
        cached = get_cached_answer(intent, db_path=self.db_path)

        self.assertEqual(cached, response2)

    def test_nonexistent_intent_returns_none(self):
        cached = get_cached_answer("intent_inconnu", db_path=self.db_path)
        self.assertIsNone(cached)

    def test_sql_injection_prevention(self):
        sql_inj_intent = "' OR '1'='1"
        response = '{"action": "none", "text": "injection test"}'

        save_answer(sql_inj_intent, response, db_path=self.db_path)
        cached = get_cached_answer(sql_inj_intent, db_path=self.db_path)
        self.assertEqual(cached, response)

        # Confirm that a different intent does not retrieve the injection payload entry
        other_cached = get_cached_answer("autre request", db_path=self.db_path)
        self.assertIsNone(other_cached)


if __name__ == "__main__":
    unittest.main()
