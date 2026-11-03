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
        user_intent = "What is the capital of France?"
        cached_response = '{"text": "Paris"}'

        save_answer(user_intent, cached_response, db_path=TEST_DB_PATH)
        result = get_cached_answer(user_intent, db_path=TEST_DB_PATH)

        self.assertEqual(result, cached_response)

    def test_get_nonexistent_cached_answer(self):
        result = get_cached_answer("Nonexistent query", db_path=TEST_DB_PATH)
        self.assertIsNone(result)

    def test_sql_injection_prevention(self):
        # Attempt SQL injection string as user_intent
        sqli_intent = "' OR '1'='1"
        save_answer(sqli_intent, "Malicious response", db_path=TEST_DB_PATH)

        # Querying an exact different intent should return None, not "Malicious response"
        self.assertIsNone(get_cached_answer("normal_intent", db_path=TEST_DB_PATH))

        # Querying the exact sqli string safely returns the stored response
        self.assertEqual(
            get_cached_answer(sqli_intent, db_path=TEST_DB_PATH),
            "Malicious response",
        )

    def test_update_existing_cache_entry(self):
        intent = "cliquer sur le bouton"
        response_v1 = '{"action": "click", "x": 100, "y": 200}'
        response_v2 = '{"action": "click", "x": 150, "y": 250}'

        save_answer(intent, response_v1, db_path=TEST_DB_PATH)
        self.assertEqual(get_cached_answer(intent, db_path=TEST_DB_PATH), response_v1)

        save_answer(intent, response_v2, db_path=TEST_DB_PATH)
        self.assertEqual(get_cached_answer(intent, db_path=TEST_DB_PATH), response_v2)

    def test_invalid_input_handling(self):
        self.assertIsNone(get_cached_answer("", db_path=TEST_DB_PATH))
        self.assertIsNone(get_cached_answer("   ", db_path=TEST_DB_PATH))
        self.assertIsNone(get_cached_answer(None, db_path=TEST_DB_PATH))

        # Should fail safely without raising exception
        save_answer(None, "response", db_path=TEST_DB_PATH)
        save_answer("intent", None, db_path=TEST_DB_PATH)
        save_answer(123, 456, db_path=TEST_DB_PATH)


if __name__ == "__main__":
    unittest.main()
