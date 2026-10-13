import os
import unittest
from database import get_cached_answer, save_answer


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        self.test_db = "test_cache.db"
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_save_and_get_cached_answer(self):
        intent = "Open music player"
        answer = '{"action": "click", "x": 100, "y": 200, "text": "Clicking player"}'

        save_answer(intent, answer, db_path=self.test_db)
        cached = get_cached_answer(intent, db_path=self.test_db)

        self.assertEqual(cached, answer)

    def test_get_nonexistent_answer(self):
        cached = get_cached_answer("Nonexistent intent", db_path=self.test_db)
        self.assertIsNone(cached)

    def test_overwrite_cached_answer(self):
        intent = "Open music player"
        answer1 = '{"action": "wait"}'
        answer2 = '{"action": "none"}'

        save_answer(intent, answer1, db_path=self.test_db)
        save_answer(intent, answer2, db_path=self.test_db)

        cached = get_cached_answer(intent, db_path=self.test_db)
        self.assertEqual(cached, answer2)

    def test_sql_injection_prevention(self):
        # SQL Injection attempt in intent parameter
        sqli_intent = "' OR '1'='1' --"
        fake_answer = "Hacked response"

        # Save an innocent record first
        save_answer("Legitimate intent", "Safe response", db_path=self.test_db)

        # Attempt to exploit via get_cached_answer
        cached = get_cached_answer(sqli_intent, db_path=self.test_db)
        self.assertIsNone(cached)

        # Attempt to exploit via save_answer
        save_answer(sqli_intent, fake_answer, db_path=self.test_db)
        cached_sqli = get_cached_answer(sqli_intent, db_path=self.test_db)
        self.assertEqual(cached_sqli, fake_answer)

        # Confirm legitimate record was not overwritten or bypassed
        legit_cached = get_cached_answer("Legitimate intent", db_path=self.test_db)
        self.assertEqual(legit_cached, "Safe response")


if __name__ == "__main__":
    unittest.main()
