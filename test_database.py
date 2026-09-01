import os
import unittest
from database import get_cached_answer, save_answer

TEST_DB = "test_cache.db"


class TestDatabase(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def tearDown(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_save_and_get_cached_answer(self):
        user_intent = "open browser"
        answer = '{"action": "click", "x": 100, "y": 200}'
        save_answer(user_intent, answer, db_path=TEST_DB)

        result = get_cached_answer(user_intent, db_path=TEST_DB)
        self.assertEqual(result, answer)

    def test_get_nonexistent_answer(self):
        result = get_cached_answer("nonexistent intent", db_path=TEST_DB)
        self.assertIsNone(result)

    def test_update_cached_answer(self):
        user_intent = "open browser"
        first_answer = '{"action": "wait"}'
        second_answer = '{"action": "none"}'

        save_answer(user_intent, first_answer, db_path=TEST_DB)
        save_answer(user_intent, second_answer, db_path=TEST_DB)

        result = get_cached_answer(user_intent, db_path=TEST_DB)
        self.assertEqual(result, second_answer)

    def test_sql_injection_prevention(self):
        injection_intent = "' OR '1'='1'; --"
        answer = '{"action": "none", "text": "safe"}'

        save_answer(injection_intent, answer, db_path=TEST_DB)

        # Confirm exact string match retrieval
        result = get_cached_answer(injection_intent, db_path=TEST_DB)
        self.assertEqual(result, answer)

        # Confirm that a different intent query doesn't match via SQL injection
        normal_query = "normal query"
        self.assertIsNone(get_cached_answer(normal_query, db_path=TEST_DB))


if __name__ == "__main__":
    unittest.main()
