import os
import tempfile
import unittest
import database


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db.close()
        self.db_path = self.temp_db.name

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_save_and_get_cached_answer(self):
        user_intent = "Open settings"
        answer = '{"action": "click", "x": 100, "y": 200, "text": "Click settings"}'

        database.save_answer(user_intent, answer, db_path=self.db_path)
        cached = database.get_cached_answer(user_intent, db_path=self.db_path)

        self.assertEqual(cached, answer)

    def test_get_nonexistent_cached_answer(self):
        cached = database.get_cached_answer("Nonexistent intent", db_path=self.db_path)
        self.assertIsNone(cached)

    def test_sql_injection_prevention(self):
        # Attempt SQL injection in user_intent
        injection_payload = "' OR '1'='1' --"
        secret_answer = "secret response"

        database.save_answer("legitimate intent", secret_answer, db_path=self.db_path)

        # Searching with injection payload should NOT return the legitimate response
        cached = database.get_cached_answer(injection_payload, db_path=self.db_path)
        self.assertIsNone(cached)

        # Attempt table drop injection payload
        drop_payload = "'; DROP TABLE answer_cache; --"
        database.save_answer(drop_payload, "safe answer", db_path=self.db_path)
        cached_drop = database.get_cached_answer(drop_payload, db_path=self.db_path)
        self.assertEqual(cached_drop, "safe answer")

        # Confirm table still exists
        legit_check = database.get_cached_answer("legitimate intent", db_path=self.db_path)
        self.assertEqual(legit_check, secret_answer)


if __name__ == "__main__":
    unittest.main()
