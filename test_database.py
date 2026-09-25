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
        intent = "Open browser"
        response = '{"action": "click", "x": 100, "y": 200, "text": "Opening browser"}'

        self.assertIsNone(get_cached_answer(intent, db_path=TEST_DB))

        save_answer(intent, response, db_path=TEST_DB)
        cached = get_cached_answer(intent, db_path=TEST_DB)

        self.assertEqual(cached, response)

    def test_sql_injection_safety(self):
        # SQL Injection attempt in user intent
        malicious_intent = "' OR '1'='1"
        malicious_response = '{"action": "none", "text": "Pwned"}'

        save_answer(malicious_intent, malicious_response, db_path=TEST_DB)

        # Normal intent should not return the malicious response
        self.assertIsNone(get_cached_answer("Normal intent", db_path=TEST_DB))

        # Querying the exact malicious intent should return its response cleanly without executing SQL injection
        self.assertEqual(
            get_cached_answer(malicious_intent, db_path=TEST_DB),
            malicious_response,
        )


if __name__ == "__main__":
    unittest.main()
