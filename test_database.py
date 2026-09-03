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
        intent = "clique sur le bouton play"
        answer = '{"action": "click", "x": 100, "y": 200, "text": "Je clique."}'

        save_answer(intent, answer, db_path=TEST_DB)
        cached = get_cached_answer(intent, db_path=TEST_DB)
        self.assertEqual(cached, answer)

    def test_get_nonexistent_intent(self):
        cached = get_cached_answer("intent_inconnu", db_path=TEST_DB)
        self.assertIsNone(cached)

    def test_update_cached_answer(self):
        intent = "ouvre le navigateur"
        save_answer(intent, "reponse 1", db_path=TEST_DB)
        save_answer(intent, "reponse 2", db_path=TEST_DB)

        cached = get_cached_answer(intent, db_path=TEST_DB)
        self.assertEqual(cached, "reponse 2")

    def test_sql_injection_prevention(self):
        sqli_intent = "' OR '1'='1"
        save_answer(sqli_intent, "safe_response", db_path=TEST_DB)

        self.assertIsNone(get_cached_answer("autre intent", db_path=TEST_DB))
        self.assertEqual(
            get_cached_answer(sqli_intent, db_path=TEST_DB), "safe_response"
        )

        drop_intent = "test'; DROP TABLE cache; --"
        save_answer(drop_intent, "safe_response_2", db_path=TEST_DB)
        self.assertEqual(
            get_cached_answer(drop_intent, db_path=TEST_DB), "safe_response_2"
        )


if __name__ == "__main__":
    unittest.main()
