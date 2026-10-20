import os
import unittest
from database import get_cached_answer, save_answer, init_db

TEST_DB = "test_cache.db"


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)
        init_db(TEST_DB)

    def tearDown(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_save_and_get_cached_answer(self):
        intent = "ouvrir le navigateur"
        answer = '{"action": "click", "x": 100, "y": 200, "text": "Ouverture du navigateur"}'
        save_answer(intent, answer, db_path=TEST_DB)

        cached = get_cached_answer(intent, db_path=TEST_DB)
        self.assertEqual(cached, answer)

    def test_get_nonexistent_answer(self):
        cached = get_cached_answer("intent_inconnu", db_path=TEST_DB)
        self.assertIsNone(cached)

    def test_sql_injection_prevention(self):
        # Malicious user intent attempting SQL injection
        malicious_intent = "test' OR '1'='1"
        malicious_answer = '{"action": "none", "text": "hacked"}'

        save_answer(malicious_intent, malicious_answer, db_path=TEST_DB)

        # Ensure query retrieves exactly the malicious intent key and doesn't match other intents
        result = get_cached_answer(malicious_intent, db_path=TEST_DB)
        self.assertEqual(result, malicious_answer)

        # Standard query should not match the malicious intent record
        normal_result = get_cached_answer("test", db_path=TEST_DB)
        self.assertIsNone(normal_result)

    def test_drop_table_injection_prevention(self):
        drop_intent = "'; DROP TABLE answer_cache; --"
        drop_answer = '{"action": "none"}'

        save_answer(drop_intent, drop_answer, db_path=TEST_DB)

        # Verify table still exists and data was safely stored
        res = get_cached_answer(drop_intent, db_path=TEST_DB)
        self.assertEqual(res, drop_answer)


if __name__ == "__main__":
    unittest.main()
