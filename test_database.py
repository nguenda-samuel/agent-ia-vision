import os
import unittest
from database import get_cached_answer, save_answer

TEST_DB_PATH = "test_cache.db"


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)

    def tearDown(self):
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)

    def test_save_and_get_cached_answer(self):
        user_intent = "Bonjour"
        response = '{"action": "none", "text": "Bonjour !"}'

        save_answer(user_intent, response, db_path=TEST_DB_PATH)
        cached = get_cached_answer(user_intent, db_path=TEST_DB_PATH)

        self.assertEqual(cached, response)

    def test_save_updates_existing_intent(self):
        user_intent = "Bonjour"
        response1 = '{"action": "none", "text": "Bonjour !"}'
        response2 = '{"action": "none", "text": "Salut !"}'

        save_answer(user_intent, response1, db_path=TEST_DB_PATH)
        save_answer(user_intent, response2, db_path=TEST_DB_PATH)

        cached = get_cached_answer(user_intent, db_path=TEST_DB_PATH)
        self.assertEqual(cached, response2)

    def test_sql_injection_prevention(self):
        sqli_intent = "Bonjour' OR '1'='1"
        response = '{"action": "none", "text": "Injected!"}'

        save_answer(sqli_intent, response, db_path=TEST_DB_PATH)

        # Ensure exact string match without SQL syntax execution
        cached = get_cached_answer(sqli_intent, db_path=TEST_DB_PATH)
        self.assertEqual(cached, response)

        # Ensure normal query doesn't match the injected string unless exact
        self.assertIsNone(get_cached_answer("Bonjour", db_path=TEST_DB_PATH))


if __name__ == "__main__":
    unittest.main()
