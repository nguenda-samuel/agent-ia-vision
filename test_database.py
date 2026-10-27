import os
import unittest
from database import get_cached_answer, save_answer

TEST_DB_PATH = "test_answers_cache.db"


class TestDatabaseSecurity(unittest.TestCase):

    def tearDown(self):
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)

    def test_save_and_get_cached_answer(self):
        intent = "Open browser"
        answer = '{"action": "click", "x": 100, "y": 200, "text": "Opening browser"}'
        save_answer(intent, answer, db_path=TEST_DB_PATH)

        cached = get_cached_answer(intent, db_path=TEST_DB_PATH)
        self.assertEqual(cached, answer)

    def test_sql_injection_safety(self):
        # Attempt SQL injection payload in user_intent
        injection_intent = "'; DROP TABLE cached_answers; --"
        answer = '{"action": "none", "text": "safe"}'

        # Save and retrieve with injection string
        save_answer(injection_intent, answer, db_path=TEST_DB_PATH)
        retrieved = get_cached_answer(injection_intent, db_path=TEST_DB_PATH)

        self.assertEqual(retrieved, answer)

        # Verify table still exists and normal query works
        save_answer("normal intent", '{"action": "none"}', db_path=TEST_DB_PATH)
        self.assertEqual(
            get_cached_answer("normal intent", db_path=TEST_DB_PATH),
            '{"action": "none"}',
        )


if __name__ == "__main__":
    unittest.main()
