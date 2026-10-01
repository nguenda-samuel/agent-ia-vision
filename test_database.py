import os
import unittest
from database import get_cached_answer, save_answer


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.test_db = "test_cache.db"
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_save_and_get_cached_answer(self):
        intent = "Open music player"
        answer = '{"action": "click", "x": 100, "y": 200, "text": "Playing music"}'

        save_answer(intent, answer, db_path=self.test_db)
        cached = get_cached_answer(intent, db_path=self.test_db)

        self.assertEqual(cached, answer)

    def test_get_nonexistent_cached_answer(self):
        cached = get_cached_answer("Nonexistent intent", db_path=self.test_db)
        self.assertIsNone(cached)

    def test_sql_injection_resilience(self):
        sql_injection_intent = "' OR '1'='1"
        answer = '{"action": "none", "text": "Safe response"}'

        save_answer(sql_injection_intent, answer, db_path=self.test_db)

        # Ensure searching for another intent doesn't return the injected intent's answer
        cached_other = get_cached_answer(
            "Other intent", db_path=self.test_db
        )
        self.assertIsNone(cached_other)

        # Ensure exact match works correctly
        cached_injected = get_cached_answer(
            sql_injection_intent, db_path=self.test_db
        )
        self.assertEqual(cached_injected, answer)


if __name__ == "__main__":
    unittest.main()
