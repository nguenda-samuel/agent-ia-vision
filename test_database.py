import os
import tempfile
import unittest
import sqlite3

from database import get_cached_answer, save_answer


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db.close()
        self.db_path = self.temp_db.name

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_save_and_get_cached_answer(self):
        intent = "ouvrir le navigateur"
        response = '{"action": "none", "text": "Ouverture du navigateur"}'

        save_answer(intent, response, db_path=self.db_path)
        cached = get_cached_answer(intent, db_path=self.db_path)

        self.assertEqual(cached, response)

    def test_get_nonexistent_answer(self):
        cached = get_cached_answer("inconnu", db_path=self.db_path)
        self.assertIsNone(cached)

    def test_sql_injection_prevention(self):
        malicious_intent = "test' UNION SELECT 'hacked' --"
        save_answer(malicious_intent, '{"action": "none"}', db_path=self.db_path)

        normal_query = "test"
        cached = get_cached_answer(normal_query, db_path=self.db_path)
        self.assertIsNone(cached)

        cached_malicious = get_cached_answer(malicious_intent, db_path=self.db_path)
        self.assertEqual(cached_malicious, '{"action": "none"}')


if __name__ == "__main__":
    unittest.main()
