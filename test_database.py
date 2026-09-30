import os
import sqlite3
import unittest
from database import get_cached_answer, save_answer

TEST_DB = "test_cache.db"


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def tearDown(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_save_and_get_cached_answer(self):
        intent = "ouvrir le navigateur"
        response = '{"action": "click", "x": 100, "y": 200, "text": "Clique sur Navigateur"}'

        save_answer(intent, response, db_path=TEST_DB)
        cached = get_cached_answer(intent, db_path=TEST_DB)
        self.assertEqual(cached, response)

    def test_update_existing_cached_answer(self):
        intent = "rechercher meteo"
        res1 = '{"text": "Meteo 1"}'
        res2 = '{"text": "Meteo 2"}'

        save_answer(intent, res1, db_path=TEST_DB)
        save_answer(intent, res2, db_path=TEST_DB)

        cached = get_cached_answer(intent, db_path=TEST_DB)
        self.assertEqual(cached, res2)

    def test_sql_injection_prevention(self):
        # Intent containing raw SQL injection payload
        malicious_intent = "test' OR '1'='1'; DROP TABLE answer_cache; --"
        response = '{"text": "safe response"}'

        # Saving answer with malicious intent
        save_answer(malicious_intent, response, db_path=TEST_DB)

        # Confirm answer can be retrieved safely
        cached = get_cached_answer(malicious_intent, db_path=TEST_DB)
        self.assertEqual(cached, response)

        # Confirm table was not dropped and normal queries still work
        with sqlite3.connect(TEST_DB) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT count(*) FROM answer_cache")
            count = cursor.fetchone()[0]
            self.assertEqual(count, 1)


if __name__ == "__main__":
    unittest.main()
