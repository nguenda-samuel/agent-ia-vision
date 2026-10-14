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

    def test_save_and_get_cached_answer(self):
        intent = "What is the capital of France?"
        answer = '{"action": "none", "text": "Paris"}'

        database.save_answer(intent, answer, db_path=self.test_db)
        cached = database.get_cached_answer(intent, db_path=self.test_db)

        self.assertEqual(cached, answer)

    def test_get_nonexistent_answer(self):
        cached = database.get_cached_answer("Nonexistent query", db_path=self.test_db)
        self.assertIsNone(cached)

    def test_sql_injection_prevention(self):
        # SQL injection payload attempting to break out or inject SQL commands
        sqli_intent = "test' OR '1'='1"
        sqli_answer = '{"action": "none", "text": "Injected"}'

        database.save_answer(sqli_intent, sqli_answer, db_path=self.test_db)

        # Ensure normal query for 'test' returns None, not the sqli entry
        cached_test = database.get_cached_answer("test", db_path=self.test_db)
        self.assertIsNone(cached_test)

        # Ensure literal lookup for the sqli payload returns sqli_answer
        cached_sqli = database.get_cached_answer(sqli_intent, db_path=self.test_db)
        self.assertEqual(cached_sqli, sqli_answer)


if __name__ == "__main__":
    unittest.main()
