import os
import unittest
from database import DB_PATH, _ensure_db_init, get_cached_answer, save_answer


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.test_db = "test_cache.db"
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_save_and_get_cached_answer(self):
        intent = "Ouvrir la calculatrice"
        answer = '{"action": "click", "x": 100, "y": 200, "text": "Ouverture"}'

        save_answer(intent, answer, db_path=self.test_db)
        cached = get_cached_answer(intent, db_path=self.test_db)

        self.assertEqual(cached, answer)

    def test_get_non_existent_answer(self):
        cached = get_cached_answer("Intent inexistant", db_path=self.test_db)
        self.assertIsNone(cached)

    def test_upsert_answer(self):
        intent = "Ouvrir la calculatrice"
        answer1 = "Reponse 1"
        answer2 = "Reponse 2"

        save_answer(intent, answer1, db_path=self.test_db)
        save_answer(intent, answer2, db_path=self.test_db)

        cached = get_cached_answer(intent, db_path=self.test_db)
        self.assertEqual(cached, answer2)


if __name__ == "__main__":
    unittest.main()
