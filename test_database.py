import os
import unittest
import database


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.test_db = "test_cache.db"
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
        database.init_db(self.test_db)

    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_save_and_get_cached_answer(self):
        intent = "ouvrir le navigateur"
        answer = '{"action": "none", "text": "Ouverture du navigateur"}'

        self.assertIsNone(database.get_cached_answer(intent, db_path=self.test_db))

        database.save_answer(intent, answer, db_path=self.test_db)

        cached = database.get_cached_answer(intent, db_path=self.test_db)
        self.assertEqual(cached, answer)

    def test_overwrite_cached_answer(self):
        intent = "cliquer sur ok"
        answer1 = '{"action": "click", "x": 100, "y": 200}'
        answer2 = '{"action": "click", "x": 150, "y": 250}'

        database.save_answer(intent, answer1, db_path=self.test_db)
        database.save_answer(intent, answer2, db_path=self.test_db)

        cached = database.get_cached_answer(intent, db_path=self.test_db)
        self.assertEqual(cached, answer2)


if __name__ == "__main__":
    unittest.main()
