import os
import unittest
from database import get_cached_answer, init_db, save_answer

TEST_DB = "test_cache.db"


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def tearDown(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_save_and_get_cached_answer(self):
        user_intent = "Ouvrir le navigateur"
        response = '{"action": "click", "x": 100, "y": 200, "text": "Ouverture du navigateur"}'

        save_answer(user_intent, response, db_path=TEST_DB)
        cached = get_cached_answer(user_intent, db_path=TEST_DB)

        self.assertEqual(cached, response)

    def test_get_nonexistent_cached_answer(self):
        cached = get_cached_answer("Commande inconnue", db_path=TEST_DB)
        self.assertIsNone(cached)

    def test_update_existing_cached_answer(self):
        user_intent = "Ouvrir le navigateur"
        response1 = '{"action": "none", "text": "Attente"}'
        response2 = '{"action": "click", "text": "Clic"}'

        save_answer(user_intent, response1, db_path=TEST_DB)
        save_answer(user_intent, response2, db_path=TEST_DB)
        cached = get_cached_answer(user_intent, db_path=TEST_DB)

        self.assertEqual(cached, response2)

    def test_sql_injection_resilience(self):
        sqli_intent = "Ouvrir' OR '1'='1"
        sqli_response = '{"action": "none", "text": "Attaque neutralisée"}'

        save_answer(sqli_intent, sqli_response, db_path=TEST_DB)

        # Ensure that searching for normal text does not return the SQLi cached response
        cached_normal = get_cached_answer("Ouvrir", db_path=TEST_DB)
        self.assertIsNone(cached_normal)

        # Ensure exact match returns the payload safely without SQL injection execution
        cached_sqli = get_cached_answer(sqli_intent, db_path=TEST_DB)
        self.assertEqual(cached_sqli, sqli_response)

    def test_sql_injection_drop_table(self):
        drop_intent = "'; DROP TABLE cache; --"
        drop_response = '{"action": "none", "text": "Safe"}'

        save_answer(drop_intent, drop_response, db_path=TEST_DB)
        cached = get_cached_answer(drop_intent, db_path=TEST_DB)
        self.assertEqual(cached, drop_response)


if __name__ == "__main__":
    unittest.main()
