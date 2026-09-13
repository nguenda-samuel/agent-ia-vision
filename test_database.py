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
        intent = "Open settings"
        response = '{"action": "click", "x": 100, "y": 200, "text": "Clicking settings"}'
        database.save_answer(intent, response, db_path=self.test_db)

        cached = database.get_cached_answer(intent, db_path=self.test_db)
        self.assertEqual(cached, response)

    def test_get_nonexistent_cached_answer(self):
        cached = database.get_cached_answer("Nonexistent", db_path=self.test_db)
        self.assertIsNone(cached)

    def test_sql_injection_prevention(self):
        sqli_intent = "'; DROP TABLE answer_cache; --"
        response = '{"action": "none", "text": "Safe response"}'
        database.save_answer(sqli_intent, response, db_path=self.test_db)

        cached = database.get_cached_answer(sqli_intent, db_path=self.test_db)
        self.assertEqual(cached, response)

        # Verify table still exists and normal entries work
        normal_cached = database.get_cached_answer("Normal intent", db_path=self.test_db)
        self.assertIsNone(normal_cached)


if __name__ == "__main__":
    unittest.main()
