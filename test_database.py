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

    def test_get_cached_answer_empty(self):
        answer = database.get_cached_answer("test query", db_path=self.test_db)
        self.assertIsNone(answer)

    def test_save_and_get_cached_answer(self):
        database.save_answer("hello", "world", db_path=self.test_db)
        answer = database.get_cached_answer("hello", db_path=self.test_db)
        self.assertEqual(answer, "world")

    def test_update_cached_answer(self):
        database.save_answer("hello", "world", db_path=self.test_db)
        database.save_answer("hello", "new world", db_path=self.test_db)
        answer = database.get_cached_answer("hello", db_path=self.test_db)
        self.assertEqual(answer, "new world")

    def test_sql_injection_safety(self):
        malicious_input = "hello' OR '1'='1"
        database.save_answer(malicious_input, "safe_answer", db_path=self.test_db)

        # Exact match should return safe_answer
        self.assertEqual(database.get_cached_answer(malicious_input, db_path=self.test_db), "safe_answer")

        # Searching another key should NOT return safe_answer (which would happen if SQL injection succeeded)
        self.assertIsNone(database.get_cached_answer("hello", db_path=self.test_db))


if __name__ == "__main__":
    unittest.main()
