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
        intent = "ouvrir le navigateur"
        response = '{"action": "none", "text": "Ouverture"}'

        save_answer(intent, response, db_path=TEST_DB)
        cached = get_cached_answer(intent, db_path=TEST_DB)

        self.assertEqual(cached, response)

    def test_update_cached_answer(self):
        intent = "ouvrir le navigateur"
        response1 = '{"action": "none", "text": "Ouverture"}'
        response2 = '{"action": "click", "x": 100, "y": 200, "text": "Clic"}'

        save_answer(intent, response1, db_path=TEST_DB)
        save_answer(intent, response2, db_path=TEST_DB)

        cached = get_cached_answer(intent, db_path=TEST_DB)
        self.assertEqual(cached, response2)

    def test_sql_injection_resistance(self):
        malicious_intent = "' OR '1'='1"
        response = '{"action": "none", "text": "Safe"}'

        save_answer(malicious_intent, response, db_path=TEST_DB)

        # Non-matching intent should return None, not leak cached response
        self.assertIsNone(get_cached_answer("autre intent", db_path=TEST_DB))
        # Exact matching malicious intent string should return the stored value safely
        self.assertEqual(get_cached_answer(malicious_intent, db_path=TEST_DB), response)


if __name__ == "__main__":
    unittest.main()
