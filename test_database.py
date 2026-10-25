import os
import unittest
import database


class TestDatabaseSecurity(unittest.TestCase):

    def setUp(self):
        database.DB_PATH = "test_cache.db"
        if os.path.exists("test_cache.db"):
            os.remove("test_cache.db")
        database._init_db()

    def tearDown(self):
        if os.path.exists("test_cache.db"):
            os.remove("test_cache.db")

    def test_save_and_get_cached_answer(self):
        query = "What is python?"
        response = '{"action": "none", "text": "Python is a programming language."}'
        database.save_answer(query, response)
        cached = database.get_cached_answer(query)
        self.assertEqual(cached, response)

    def test_get_non_existent_key(self):
        self.assertIsNone(database.get_cached_answer("non_existent_query"))

    def test_sql_injection_prevention(self):
        injection_query = "test' OR '1'='1"
        injection_response = "injected_data"

        database.save_answer(injection_query, injection_response)

        self.assertEqual(
            database.get_cached_answer(injection_query), injection_response
        )
        self.assertIsNone(database.get_cached_answer("test"))


if __name__ == "__main__":
    unittest.main()
