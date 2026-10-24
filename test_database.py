import os
import tempfile
import unittest
import database


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")
        os.close(self.db_fd)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_save_and_get_cached_answer(self):
        intent = "test intent"
        answer = '{"action": "none", "text": "hello"}'
        database.save_answer(intent, answer, db_path=self.db_path)

        cached = database.get_cached_answer(intent, db_path=self.db_path)
        self.assertEqual(cached, answer)

    def test_sql_injection_resilience(self):
        # Intent with SQL injection attempt
        sqli_intent = "test' OR '1'='1"
        answer = '{"action": "none", "text": "secret"}'
        database.save_answer(sqli_intent, answer, db_path=self.db_path)

        # Non-matching intent should not return the answer despite SQLi syntax
        self.assertIsNone(database.get_cached_answer("test", db_path=self.db_path))
        self.assertEqual(database.get_cached_answer(sqli_intent, db_path=self.db_path), answer)

    def test_update_existing_cache(self):
        intent = "duplicate intent"
        answer1 = "answer 1"
        answer2 = "answer 2"
        database.save_answer(intent, answer1, db_path=self.db_path)
        database.save_answer(intent, answer2, db_path=self.db_path)

        cached = database.get_cached_answer(intent, db_path=self.db_path)
        self.assertEqual(cached, answer2)


if __name__ == "__main__":
    unittest.main()
