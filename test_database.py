import os
import tempfile
import unittest
import database


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")
        os.close(self.db_fd)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_save_and_get_cached_answer(self):
        intent = "Affiche la météo"
        response = '{"action": "none", "text": "Il fait beau."}'
        database.save_answer(intent, response, db_path=self.db_path)
        cached = database.get_cached_answer(intent, db_path=self.db_path)
        self.assertEqual(cached, response)

    def test_get_nonexistent_cached_answer(self):
        cached = database.get_cached_answer("Commande inconnue", db_path=self.db_path)
        self.assertIsNone(cached)

    def test_sql_injection_safety(self):
        normal_intent = "Ouvre le navigateur"
        normal_response = '{"action": "none", "text": "Navigateur ouvert."}'
        database.save_answer(normal_intent, normal_response, db_path=self.db_path)

        sqli_intent = "' OR '1'='1"
        cached = database.get_cached_answer(sqli_intent, db_path=self.db_path)
        self.assertIsNone(cached)

        sqli_save_intent = "test'; DROP TABLE answer_cache; --"
        sqli_response = "safe_text"
        database.save_answer(sqli_save_intent, sqli_response, db_path=self.db_path)

        # Confirm the table was not dropped and queries still work safely
        cached_normal = database.get_cached_answer(normal_intent, db_path=self.db_path)
        self.assertEqual(cached_normal, normal_response)
        cached_sqli = database.get_cached_answer(sqli_save_intent, db_path=self.db_path)
        self.assertEqual(cached_sqli, sqli_response)


if __name__ == "__main__":
    unittest.main()
