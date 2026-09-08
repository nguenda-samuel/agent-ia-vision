import os
import unittest
import database


class TestDatabase(unittest.TestCase):

    def setUp(self):
        # Use a temporary test db path if needed
        self.original_db = database.DB_PATH
        database.DB_PATH = "test_cache.db"
        if os.path.exists("test_cache.db"):
            os.remove("test_cache.db")

    def tearDown(self):
        database.DB_PATH = self.original_db
        if os.path.exists("test_cache.db"):
            os.remove("test_cache.db")

    def test_save_and_get_cached_answer(self):
        self.assertIsNone(database.get_cached_answer("test query"))
        database.save_answer("test query", "cached response")
        self.assertEqual(
            database.get_cached_answer("test query"), "cached response"
        )

    def test_update_cached_answer(self):
        database.save_answer("test query", "response 1")
        database.save_answer("test query", "response 2")
        self.assertEqual(
            database.get_cached_answer("test query"), "response 2"
        )


if __name__ == "__main__":
    unittest.main()
