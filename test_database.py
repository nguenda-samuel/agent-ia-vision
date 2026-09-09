import os
import tempfile
import unittest
import database


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db.close()
        self.db_path = self.temp_db.name

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_save_and_get_cached_answer(self):
        user_intent = "Open settings"
        answer = '{"action": "click", "x": 100, "y": 200, "text": "Click settings"}'

        database.save_answer(user_intent, answer, db_path=self.db_path)
        cached = database.get_cached_answer(user_intent, db_path=self.db_path)

        self.assertEqual(cached, answer)

    def test_get_nonexistent_cached_answer(self):
        cached = database.get_cached_answer("Nonexistent intent", db_path=self.db_path)
        self.assertIsNone(cached)


if __name__ == "__main__":
    unittest.main()
