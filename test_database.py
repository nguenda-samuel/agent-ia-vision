import os
import sqlite3
import unittest
from database import get_cached_answer, save_answer


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        self.db_path = "test_cache.db"
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_save_and_get_cached_answer(self):
        intent = "Open Google Chrome"
        answer = '{"action": "click", "x": 100, "y": 200}'

        # Initially non-existent
        cached = get_cached_answer(intent, db_path=self.db_path)
        self.assertIsNone(cached)

        # Save answer
        save_answer(intent, answer, db_path=self.db_path)

        # Retrieve answer
        cached = get_cached_answer(intent, db_path=self.db_path)
        self.assertEqual(cached, answer)

    def test_update_cached_answer(self):
        intent = "Open Settings"
        answer1 = '{"action": "click", "x": 10, "y": 20}'
        answer2 = '{"action": "click", "x": 30, "y": 40}'

        save_answer(intent, answer1, db_path=self.db_path)
        save_answer(intent, answer2, db_path=self.db_path)

        cached = get_cached_answer(intent, db_path=self.db_path)
        self.assertEqual(cached, answer2)


if __name__ == "__main__":
    unittest.main()
