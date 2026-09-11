import os
import unittest
import database


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        self.test_db = "test_cache.db"
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_save_and_get_cached_answer(self):
        intent = "ouvrir le navigateur"
        response = '{"action": "click", "x": 100, "y": 200, "text": "Ouverture du navigateur"}'
        database.save_answer(intent, response, db_path=self.test_db)

        cached = database.get_cached_answer(intent, db_path=self.test_db)
        self.assertEqual(cached, response)

    def test_get_nonexistent_cached_answer(self):
        cached = database.get_cached_answer("intent_inconnu", db_path=self.test_db)
        self.assertIsNone(cached)

    def test_save_answer_upsert(self):
        intent = "ouvrir le navigateur"
        initial_resp = "réponse initiale"
        updated_resp = "réponse mise à jour"

        database.save_answer(intent, initial_resp, db_path=self.test_db)
        database.save_answer(intent, updated_resp, db_path=self.test_db)

        cached = database.get_cached_answer(intent, db_path=self.test_db)
        self.assertEqual(cached, updated_resp)

    def test_sql_injection_prevention(self):
        sqli_intent = "test' OR '1'='1"
        response = "réponse sécurisée"

        database.save_answer(sqli_intent, response, db_path=self.test_db)

        # La recherche par intent malveillant doit retourner uniquement sa propre entrée
        cached = database.get_cached_answer(sqli_intent, db_path=self.test_db)
        self.assertEqual(cached, response)

        # Un intent ordinaire ne doit pas correspondre
        cached_normal = database.get_cached_answer("autre_intent", db_path=self.test_db)
        self.assertIsNone(cached_normal)


if __name__ == "__main__":
    unittest.main()
