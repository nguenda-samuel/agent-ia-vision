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
        response = '{"action": "click", "x": 100, "y": 200, "text": "Ouverture"}'

        self.assertIsNone(database.get_cached_answer(intent, db_path=self.test_db))

        database.save_answer(intent, response, db_path=self.test_db)

        cached = database.get_cached_answer(intent, db_path=self.test_db)
        self.assertEqual(cached, response)

    def test_update_cached_answer(self):
        intent = "ouvrir le navigateur"
        response1 = '{"action": "none", "text": "Premier"}'
        response2 = '{"action": "none", "text": "Deuxième"}'

        database.save_answer(intent, response1, db_path=self.test_db)
        database.save_answer(intent, response2, db_path=self.test_db)

        cached = database.get_cached_answer(intent, db_path=self.test_db)
        self.assertEqual(cached, response2)

    def test_sql_injection_prevention(self):
        sql_injection_intent = "test'; DROP TABLE answer_cache; --"
        response = '{"action": "none", "text": "Safe"}'

        database.save_answer(sql_injection_intent, response, db_path=self.test_db)

        cached = database.get_cached_answer(sql_injection_intent, db_path=self.test_db)
        self.assertEqual(cached, response)

        # Confirm answer_cache table still exists and normal query works
        normal_intent = "normal_intent"
        database.save_answer(normal_intent, response, db_path=self.test_db)
        self.assertEqual(database.get_cached_answer(normal_intent, db_path=self.test_db), response)


if __name__ == "__main__":
    unittest.main()
