import os
import tempfile
import unittest

from database import get_cached_answer, save_answer


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        self.db_file = tempfile.NamedTemporaryFile(delete=False)
        self.db_path = self.db_file.name
        self.db_file.close()

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_cache_miss_returns_none(self):
        result = get_cached_answer("non_existent_intent", db_path=self.db_path)
        self.assertIsNone(result)

    def test_save_and_get_cached_answer(self):
        intent = "ouvrir le navigateur"
        answer = '{"action": "click", "x": 100, "y": 200, "text": "Ouverture"}'
        save_answer(intent, answer, db_path=self.db_path)

        cached = get_cached_answer(intent, db_path=self.db_path)
        self.assertEqual(cached, answer)


if __name__ == "__main__":
    unittest.main()
