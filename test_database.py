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
        user_intent = "What is Python?"
        answer = '{"action": "none", "text": "Python is a programming language."}'

        save_answer(user_intent, answer, db_path=TEST_DB_PATH)
        cached = get_cached_answer(user_intent, db_path=TEST_DB_PATH)

        self.assertEqual(cached, answer)

    def test_sql_injection_safety(self):
        # Malicious input attempting SQL injection
        sql_injection_intent = "' OR '1'='1' --"
        answer = '{"action": "none", "text": "Safe response"}'

        save_answer(sql_injection_intent, answer, db_path=TEST_DB_PATH)

        # Ensure normal query for a different intent does not return the injected row
        other = get_cached_answer("normal intent", db_path=TEST_DB_PATH)
        self.assertIsNone(other)

        # Ensure retrieving with exact string works safely
        retrieved = get_cached_answer(sql_injection_intent, db_path=TEST_DB_PATH)
        self.assertEqual(retrieved, answer)

    def test_update_on_conflict(self):
        user_intent = "Open browser"
        answer1 = '{"action": "click", "x": 10, "y": 20}'
        answer2 = '{"action": "click", "x": 50, "y": 60}'

        save_answer(user_intent, answer1, db_path=TEST_DB_PATH)
        save_answer(user_intent, answer2, db_path=TEST_DB_PATH)

        cached = get_cached_answer(user_intent, db_path=TEST_DB_PATH)
        self.assertEqual(cached, answer2)


if __name__ == "__main__":
    unittest.main()
