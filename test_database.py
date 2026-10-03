import os
import tempfile
import unittest
import database


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.db_path = self.temp_db.name
        self.temp_db.close()

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_save_and_get_cached_answer(self):
        database.save_answer("test_intent", "test_answer", db_path=self.db_path)
        ans = database.get_cached_answer("test_intent", db_path=self.db_path)
        self.assertEqual(ans, "test_answer")

    def test_get_nonexistent_answer(self):
        ans = database.get_cached_answer("nonexistent", db_path=self.db_path)
        self.assertIsNone(ans)


if __name__ == "__main__":
    unittest.main()
