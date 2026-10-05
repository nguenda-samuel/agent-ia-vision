import os
import unittest
import database


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        self.test_db = "test_cache.db"
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_save_and_get_cached_answer(self):
        intent = "play music"
        answer = '{"action": "click", "x": 100, "y": 200, "text": "Playing music"}'

        database.save_answer(intent, answer, db_name=self.test_db)
        cached = database.get_cached_answer(intent, db_name=self.test_db)

        self.assertEqual(cached, answer)

    def test_missing_cache_returns_none(self):
        cached = database.get_cached_answer("nonexistent", db_name=self.test_db)
        self.assertIsNone(cached)

    def test_sql_injection_safety(self):
        # SQL injection payloads in user intent
        sqli_intent_1 = "' OR '1'='1"
        sqli_intent_2 = "test'; DROP TABLE answer_cache; --"
        answer = '{"action": "none", "text": "safe response"}'

        database.save_answer(sqli_intent_1, answer, db_name=self.test_db)

        # Non-matching query should return None rather than bypassing query filtering
        self.assertIsNone(
            database.get_cached_answer("normal query", db_name=self.test_db)
        )

        # Exact matching query returns saved response
        self.assertEqual(
            database.get_cached_answer(sqli_intent_1, db_name=self.test_db),
            answer,
        )

        # Ensure DROP TABLE payload did not execute drop table
        database.save_answer(sqli_intent_2, answer, db_name=self.test_db)
        self.assertEqual(
            database.get_cached_answer(sqli_intent_2, db_name=self.test_db),
            answer,
        )


if __name__ == "__main__":
    unittest.main()
