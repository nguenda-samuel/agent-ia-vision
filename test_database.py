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
        response = '{"action": "none", "text": "Opening browser"}'

        save_answer(intent, response, db_path=TEST_DB)
        cached = get_cached_answer(intent, db_path=TEST_DB)
        self.assertEqual(cached, response)

    def test_update_existing_cache(self):
        intent = "Open browser"
        response1 = '{"action": "none", "text": "First response"}'
        response2 = '{"action": "none", "text": "Updated response"}'

        save_answer(intent, response1, db_path=TEST_DB)
        save_answer(intent, response2, db_path=TEST_DB)

        cached = get_cached_answer(intent, db_path=TEST_DB)
        self.assertEqual(cached, response2)

    def test_sql_injection_prevention(self):
        malicious_intent = "' OR '1'='1"
        response = '{"action": "none", "text": "Safe response"}'

        save_answer(malicious_intent, response, db_path=TEST_DB)
        cached_malicious = get_cached_answer(malicious_intent, db_path=TEST_DB)
        self.assertEqual(cached_malicious, response)

        cached_normal = get_cached_answer("Normal query", db_path=TEST_DB)
        self.assertIsNone(cached_normal)


if __name__ == "__main__":
    unittest.main()
