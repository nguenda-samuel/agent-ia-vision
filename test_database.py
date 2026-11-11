import os
import unittest
import database


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        self.db_path = "test_cache.db"
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_save_and_get_cached_answer(self):
        user_intent = "Open browser"
        response = '{"action": "click", "x": 100, "y": 200, "text": "Opening browser"}'

        database.save_answer(user_intent, response, db_path=self.db_path)
        cached = database.get_cached_answer(user_intent, db_path=self.db_path)

        self.assertEqual(cached, response)

    def test_save_answer_conflict_update(self):
        user_intent = "Open browser"
        resp1 = '{"action": "click"}'
        resp2 = '{"action": "wait"}'

        database.save_answer(user_intent, resp1, db_path=self.db_path)
        self.assertEqual(
            database.get_cached_answer(user_intent, db_path=self.db_path), resp1
        )

        database.save_answer(user_intent, resp2, db_path=self.db_path)
        self.assertEqual(
            database.get_cached_answer(user_intent, db_path=self.db_path), resp2
        )

    def test_sqli_resilience(self):
        sqli_intent = "test' OR '1'='1"
        response = "safe response"

        database.save_answer(sqli_intent, response, db_path=self.db_path)
        cached = database.get_cached_answer(sqli_intent, db_path=self.db_path)

        self.assertEqual(cached, response)

        # Ensure that SQL injection payload did not match unintended rows
        non_existent = database.get_cached_answer(
            "another intent' OR '1'='1", db_path=self.db_path
        )
        self.assertIsNone(non_existent)

    def test_invalid_input_types(self):
        self.assertIsNone(database.get_cached_answer(None, db_path=self.db_path))
        self.assertIsNone(database.get_cached_answer(12345, db_path=self.db_path))

        with self.assertRaises(TypeError):
            database.save_answer(None, "response", db_path=self.db_path)

        with self.assertRaises(TypeError):
            database.save_answer("intent", None, db_path=self.db_path)


if __name__ == "__main__":
    unittest.main()
