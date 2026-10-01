import os
import sqlite3
import tempfile
import unittest

from database import get_cached_answer, init_db, save_answer


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()
        init_db(self.db_path)

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_get_cached_answer_missing(self):
        result = get_cached_answer("Ouvrir navigateur", db_path=self.db_path)
        self.assertIsNone(result)

    def test_save_and_get_cached_answer(self):
        intent = "Lancer la musique"
        answer = '{"action": "click", "x": 100, "y": 200, "text": "Lancement"}'
        save_answer(intent, answer, db_path=self.db_path)

        cached = get_cached_answer(intent, db_path=self.db_path)
        self.assertEqual(cached, answer)

    def test_save_answer_replace_existing(self):
        intent = "Rechercher"
        answer1 = '{"action": "none", "text": "V1"}'
        answer2 = '{"action": "click", "x": 50, "y": 50, "text": "V2"}'

        save_answer(intent, answer1, db_path=self.db_path)
        save_answer(intent, answer2, db_path=self.db_path)

        cached = get_cached_answer(intent, db_path=self.db_path)
        self.assertEqual(cached, answer2)

    def test_sql_injection_protection(self):
        sqli_intent = "' OR '1'='1"
        answer = '{"action": "none", "text": "Safe"}'
        save_answer(sqli_intent, answer, db_path=self.db_path)

        # Confirm exact match retrieved, not all records
        cached = get_cached_answer(sqli_intent, db_path=self.db_path)
        self.assertEqual(cached, answer)

        # Confirm non-existent query does not match via SQL injection
        other_query = "' OR '1'='1' --"
        self.assertIsNone(get_cached_answer(other_query, db_path=self.db_path))

        # Confirm drop table injection attempt does not drop the table
        drop_attempt = "test'; DROP TABLE cache; --"
        save_answer(drop_attempt, answer, db_path=self.db_path)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT count(*) FROM cache")
            count = cursor.fetchone()[0]
            self.assertEqual(count, 2)


if __name__ == "__main__":
    unittest.main()
