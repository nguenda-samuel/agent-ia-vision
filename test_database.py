import os
import unittest
from database import get_cached_answer, save_answer

TEST_DB = "test_cache.db"


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def tearDown(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_save_and_get_cached_answer(self):
        user_intent = "Ouvrir le navigateur web"
        expected_response = '{"action": "click", "x": 100, "y": 200, "text": "Ouverture"}'

        self.assertIsNone(get_cached_answer(user_intent, db_path=TEST_DB))

        save_answer(user_intent, expected_response, db_path=TEST_DB)
        cached = get_cached_answer(user_intent, db_path=TEST_DB)
        self.assertEqual(cached, expected_response)

    def test_update_cached_answer(self):
        user_intent = "Ouvrir le navigateur web"
        initial_response = '{"action": "none"}'
        updated_response = '{"action": "click", "x": 50, "y": 50}'

        save_answer(user_intent, initial_response, db_path=TEST_DB)
        self.assertEqual(get_cached_answer(user_intent, db_path=TEST_DB), initial_response)

        save_answer(user_intent, updated_response, db_path=TEST_DB)
        self.assertEqual(get_cached_answer(user_intent, db_path=TEST_DB), updated_response)

    def test_sql_injection_payload_safety(self):
        sqli_intent = "' OR '1'='1' --"
        response_text = '{"action": "none", "text": "Sécurisé"}'

        save_answer(sqli_intent, response_text, db_path=TEST_DB)

        # Retrieval with exact string should work
        self.assertEqual(get_cached_answer(sqli_intent, db_path=TEST_DB), response_text)

        # Non-matching intent should return None, showing SQL injection attempt failed to leak data
        self.assertIsNone(get_cached_answer("Autre intent", db_path=TEST_DB))


if __name__ == "__main__":
    unittest.main()
