import os
import unittest
from database import get_cached_answer, save_answer

TEST_DB = "test_agent_cache.db"


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def tearDown(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_save_and_get_cached_answer(self):
        intent = "How to open settings?"
        answer = "Click on the gear icon."
        save_answer(intent, answer, db_path=TEST_DB)
        cached = get_cached_answer(intent, db_path=TEST_DB)
        self.assertEqual(cached, answer)

    def test_update_existing_cache(self):
        intent = "Open file"
        answer1 = "Click File"
        answer2 = "Click File -> Open"
        save_answer(intent, answer1, db_path=TEST_DB)
        save_answer(intent, answer2, db_path=TEST_DB)
        cached = get_cached_answer(intent, db_path=TEST_DB)
        self.assertEqual(cached, answer2)

    def test_sql_injection_safety(self):
        sqli_intent = "' OR '1'='1'; --"
        answer = "Safe response"
        save_answer(sqli_intent, answer, db_path=TEST_DB)

        # Ensure normal query doesn't match all records or execute payload
        self.assertIsNone(get_cached_answer("normal_intent", db_path=TEST_DB))
        self.assertEqual(get_cached_answer(sqli_intent, db_path=TEST_DB), answer)


if __name__ == "__main__":
    unittest.main()
