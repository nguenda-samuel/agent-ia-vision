import os
import unittest
import database


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        self.db_path = "test_cache.db"
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_save_and_get_cached_answer(self):
        user_intent = "Open browser"
        response = '{"action": "click", "x": 100, "y": 200, "text": "Opening browser"}'

        database.save_answer(user_intent, response, db_path=self.db_path)
        cached = database.get_cached_answer(user_intent, db_path=self.db_path)

        self.assertEqual(cached, response)

    def test_sqli_resilience(self):
        sqli_intent = "test' OR '1'='1"
        response = "safe response"

        database.save_answer(sqli_intent, response, db_path=self.db_path)
        cached = database.get_cached_answer(sqli_intent, db_path=self.db_path)

        self.assertEqual(cached, response)

        non_existent = database.get_cached_answer("another intent' OR '1'='1", db_path=self.db_path)
        self.assertIsNone(non_existent)


if __name__ == "__main__":
    unittest.main()
