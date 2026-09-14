import os
import sqlite3
import tempfile
import unittest

from database import get_cached_answer, save_answer


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.db_path = self.temp_db.name
        self.temp_db.close()

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_save_and_get_cached_answer(self):
        user_intent = "Ouvrir le navigateur"
        cached_response = '{"action": "click", "x": 100, "y": 200, "text": "Je clique"}'

        # Verify no entry initially
        self.assertIsNone(get_cached_answer(user_intent, db_path=self.db_path))

        # Save and verify retrieval
        save_answer(user_intent, cached_response, db_path=self.db_path)
        retrieved = get_cached_answer(user_intent, db_path=self.db_path)
        self.assertEqual(retrieved, cached_response)

    def test_update_cached_answer(self):
        user_intent = "Ouvrir le navigateur"
        initial_response = '{"action": "none"}'
        updated_response = '{"action": "click", "x": 50, "y": 50}'

        save_answer(user_intent, initial_response, db_path=self.db_path)
        self.assertEqual(get_cached_answer(user_intent, db_path=self.db_path), initial_response)

        save_answer(user_intent, updated_response, db_path=self.db_path)
        self.assertEqual(get_cached_answer(user_intent, db_path=self.db_path), updated_response)

    def test_sql_injection_prevention(self):
        sqli_intent = "test' OR '1'='1"
        sqli_response = "injected_response"

        save_answer(sqli_intent, sqli_response, db_path=self.db_path)

        # Retrieve with exact intent
        self.assertEqual(get_cached_answer(sqli_intent, db_path=self.db_path), sqli_response)

        # Verify that querying a different intent doesn't return the injected answer
        self.assertIsNone(get_cached_answer("normal_intent", db_path=self.db_path))


if __name__ == "__main__":
    unittest.main()
