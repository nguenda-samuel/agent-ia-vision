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

    def test_get_and_save_answer(self):
        intent = "test_intent"
        response = '{"action": "none", "text": "hello"}'

        self.assertIsNone(database.get_cached_answer(intent, db_path=self.test_db))

        database.save_answer(intent, response, db_path=self.test_db)
        cached = database.get_cached_answer(intent, db_path=self.test_db)

        self.assertEqual(cached, response)

    def test_update_answer(self):
        intent = "test_intent"
        response1 = '{"action": "none", "text": "first"}'
        response2 = '{"action": "none", "text": "second"}'

        database.save_answer(intent, response1, db_path=self.test_db)
        database.save_answer(intent, response2, db_path=self.test_db)

        cached = database.get_cached_answer(intent, db_path=self.test_db)
        self.assertEqual(cached, response2)


if __name__ == "__main__":
    unittest.main()
