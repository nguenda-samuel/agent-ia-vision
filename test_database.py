import os
import unittest
import database

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

        database.save_answer(user_intent, response, db_path=TEST_DB)
        cached = database.get_cached_answer(user_intent, db_path=TEST_DB)

        self.assertEqual(cached, response)

    def test_sql_injection_prevention(self):
        # Test input with SQL injection payload
        malicious_intent = "Ouvrir' OR '1'='1"
        malicious_response = "hacked"

        database.save_answer(malicious_intent, malicious_response, db_path=TEST_DB)

        # Normal query should not return malicious result for a different query
        normal_query_result = database.get_cached_answer("Normal query", db_path=TEST_DB)
        self.assertIsNone(normal_query_result)

        # Querying the exact string safely returns the stored response without executing SQL injection
        exact_query_result = database.get_cached_answer(malicious_intent, db_path=TEST_DB)
        self.assertEqual(exact_query_result, malicious_response)


if __name__ == "__main__":
    unittest.main()
