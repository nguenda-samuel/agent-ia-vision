import os
import unittest
import database

TEST_DB = "test_cache.db"


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def tearDown(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_save_and_get_cached_answer(self):
        intent = "Open settings"
        answer = '{"action": "click", "x": 100, "y": 200, "text": "Opening settings"}'

        self.assertIsNone(database.get_cached_answer(intent, db_path=TEST_DB))
        database.save_answer(intent, answer, db_path=TEST_DB)
        cached = database.get_cached_answer(intent, db_path=TEST_DB)
        self.assertEqual(cached, answer)

    def test_save_answer_update_existing(self):
        intent = "Open settings"
        answer1 = '{"action": "none"}'
        answer2 = '{"action": "click", "x": 10, "y": 20}'

        database.save_answer(intent, answer1, db_path=TEST_DB)
        database.save_answer(intent, answer2, db_path=TEST_DB)
        cached = database.get_cached_answer(intent, db_path=TEST_DB)
        self.assertEqual(cached, answer2)

    def test_sql_injection_prevention(self):
        sqli_intent = "' OR '1'='1"
        sqli_answer = "Malicious Payload"

        database.save_answer(sqli_intent, sqli_answer, db_path=TEST_DB)
        cached = database.get_cached_answer(sqli_intent, db_path=TEST_DB)
        self.assertEqual(cached, sqli_answer)

        # Ensure normal query doesn't match all entries due to injection
        normal_intent = "Normal intent"
        self.assertIsNone(database.get_cached_answer(normal_intent, db_path=TEST_DB))


if __name__ == "__main__":
    unittest.main()
