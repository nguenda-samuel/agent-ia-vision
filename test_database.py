import os
import tempfile
import unittest
from database import get_cached_answer, save_answer


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_save_and_get_cached_answer(self):
        intent = "Comment ouvrir un fichier ?"
        response = "Cliquez sur Fichier -> Ouvrir"
        save_answer(intent, response, db_path=self.db_path)

        cached = get_cached_answer(intent, db_path=self.db_path)
        self.assertEqual(cached, response)

    def test_sql_injection_safety(self):
        sqli_intent = "' OR '1'='1"
        response = "Secret Response"
        save_answer(sqli_intent, response, db_path=self.db_path)

        # Retrieval with exact string should work
        cached = get_cached_answer(sqli_intent, db_path=self.db_path)
        self.assertEqual(cached, response)

        # Retrieval with a different intent should return None, not leak cached data via SQLi
        other_cached = get_cached_answer("normal intent", db_path=self.db_path)
        self.assertIsNone(other_cached)


if __name__ == "__main__":
    unittest.main()
