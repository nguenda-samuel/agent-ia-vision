import os
import unittest
import database


class TestDatabaseSecurity(unittest.TestCase):

    def setUp(self):
        database.DB_PATH = "test_answers_cache.db"
        if os.path.exists(database.DB_PATH):
            os.remove(database.DB_PATH)

    def tearDown(self):
        if os.path.exists(database.DB_PATH):
            os.remove(database.DB_PATH)

    def test_save_and_get_cached_answer(self):
        intent = "Open settings menu"
        answer = '{"action": "click", "x": 10, "y": 20, "text": "Click settings"}'
        database.save_answer(intent, answer)
        cached = database.get_cached_answer(intent)
        self.assertEqual(cached, answer)

    def test_sql_injection_prevention(self):
        # Attempt SQL injection payloads
        sql_payloads = [
            "' OR '1'='1",
            "'; DROP TABLE answers_cache; --",
            "\" UNION SELECT answer FROM answers_cache --",
        ]
        for payload in sql_payloads:
            database.save_answer(payload, '{"action": "none", "text": "safe"}')
            cached = database.get_cached_answer(payload)
            self.assertEqual(cached, '{"action": "none", "text": "safe"}')

        # Confirm table still exists and wasn't dropped or altered
        cached_normal = database.get_cached_answer("non_existent_intent")
        self.assertIsNone(cached_normal)

    def test_invalid_input_handling(self):
        self.assertIsNone(database.get_cached_answer(None))
        self.assertIsNone(database.get_cached_answer(12345))
        self.assertIsNone(database.get_cached_answer(""))
        self.assertIsNone(database.get_cached_answer("   "))

        # Test saving invalid input
        database.save_answer(None, "response")
        database.save_answer("intent", None)
        database.save_answer("", "response")

    def test_input_length_limit(self):
        long_intent = "A" * 2000
        database.save_answer(long_intent, "long_response")

        # The intent should be truncated to 1000 characters
        self.assertEqual(
            database.get_cached_answer(long_intent), "long_response"
        )
        self.assertEqual(
            database.get_cached_answer("A" * 1000), "long_response"
        )


if __name__ == "__main__":
    unittest.main()
