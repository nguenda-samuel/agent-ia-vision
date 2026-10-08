import os
import tempfile
import unittest
from database import get_cached_answer, init_db, save_answer


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db.close()
        self.db_path = self.temp_db.name
        init_db(self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_get_cached_answer_empty(self):
        result = get_cached_answer("Non-existent intent", db_path=self.db_path)
        self.assertIsNone(result)

    def test_save_and_get_cached_answer(self):
        intent = "Open Settings"
        response = '{"action": "click", "x": 10, "y": 20, "text": "Clicking settings"}'
        save_answer(intent, response, db_path=self.db_path)

        cached = get_cached_answer(intent, db_path=self.db_path)
        self.assertEqual(cached, response)

    def test_overwrite_cached_answer(self):
        intent = "Open Settings"
        response1 = '{"action": "none", "text": "Waiting"}'
        response2 = '{"action": "click", "x": 100, "y": 200, "text": "Clicked"}'

        save_answer(intent, response1, db_path=self.db_path)
        save_answer(intent, response2, db_path=self.db_path)

        cached = get_cached_answer(intent, db_path=self.db_path)
        self.assertEqual(cached, response2)

    def test_sql_injection_prevention_get(self):
        # Save a valid answer
        save_answer("valid intent", "valid response", db_path=self.db_path)

        # Attempt SQL injection in get_cached_answer
        sqli_payload = "valid intent' OR '1'='1"
        result = get_cached_answer(sqli_payload, db_path=self.db_path)
        self.assertIsNone(result)

    def test_sql_injection_prevention_save(self):
        sqli_intent = "test'; DROP TABLE cache; --"
        sqli_response = "harmless response"

        # Save with SQL injection payload
        save_answer(sqli_intent, sqli_response, db_path=self.db_path)

        # Ensure table was not dropped and data is safely retrieved
        retrieved = get_cached_answer(sqli_intent, db_path=self.db_path)
        self.assertEqual(retrieved, sqli_response)


if __name__ == "__main__":
    unittest.main()
