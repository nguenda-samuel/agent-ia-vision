import os
import unittest
from database import get_cached_answer, save_answer
import ai_engine

TEST_DB = "test_agent_memory.db"


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def tearDown(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_save_and_get_cached_answer(self):
        save_answer("hello world", "response 1", db_path=TEST_DB)
        res = get_cached_answer("hello world", db_path=TEST_DB)
        self.assertEqual(res, "response 1")

    def test_overwrite_cached_answer(self):
        save_answer("query 1", "response A", db_path=TEST_DB)
        save_answer("query 1", "response B", db_path=TEST_DB)
        res = get_cached_answer("query 1", db_path=TEST_DB)
        self.assertEqual(res, "response B")

    def test_sql_injection_prevention(self):
        sqli_intent = "test' OR '1'='1"
        save_answer(sqli_intent, "safe response", db_path=TEST_DB)

        # Confirm exact match works and non-matching query returns None (not leaking all rows)
        self.assertEqual(
            get_cached_answer(sqli_intent, db_path=TEST_DB), "safe response"
        )
        self.assertIsNone(get_cached_answer("other intent", db_path=TEST_DB))

    def test_ai_engine_integration(self):
        # Verify ai_engine successfully imports and uses database caching functions
        self.assertEqual(ai_engine.get_cached_answer, get_cached_answer)
        self.assertEqual(ai_engine.save_answer, save_answer)


if __name__ == "__main__":
    unittest.main()
