import os
import sqlite3
import tempfile
import unittest

from database import get_cached_answer, save_answer


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_save_and_get_cached_answer(self):
        intent = "ouvrir le navigateur"
        response = '{"action": "none", "text": "Ouverture du navigateur"}'

        self.assertIsNone(get_cached_answer(intent, db_path=self.db_path))

        save_answer(intent, response, db_path=self.db_path)

        cached = get_cached_answer(intent, db_path=self.db_path)
        self.assertEqual(cached, response)

    def test_sql_injection_prevention(self):
        sqli_intent = "test' OR '1'='1"
        sqli_response = '{"action": "none", "text": "Injection test"}'

        save_answer(sqli_intent, sqli_response, db_path=self.db_path)

        # Retrieve exact match using parameterized query
        cached = get_cached_answer(sqli_intent, db_path=self.db_path)
        self.assertEqual(cached, sqli_response)

        # Non-matching intent should return None, not trigger SQL syntax error or leak rows
        other_cached = get_cached_answer("normal_intent", db_path=self.db_path)
        self.assertIsNone(other_cached)

    def test_update_existing_cache(self):
        intent = "cliquer sur le bouton"
        resp1 = '{"action": "click", "x": 100, "y": 200}'
        resp2 = '{"action": "click", "x": 150, "y": 250}'

        save_answer(intent, resp1, db_path=self.db_path)
        self.assertEqual(get_cached_answer(intent, db_path=self.db_path), resp1)

        save_answer(intent, resp2, db_path=self.db_path)
        self.assertEqual(get_cached_answer(intent, db_path=self.db_path), resp2)


if __name__ == "__main__":
    unittest.main()
