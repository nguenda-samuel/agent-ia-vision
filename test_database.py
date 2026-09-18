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
        intent = "Ouvrir le navigateur"
        response = '{"action": "click", "x": 100, "y": 200, "text": "Ouverture"}'

        save_answer(intent, response, db_path=self.db_path)
        cached = get_cached_answer(intent, db_path=self.db_path)

        self.assertEqual(cached, response)

    def test_get_nonexistent_answer(self):
        cached = get_cached_answer("Inexistant", db_path=self.db_path)
        self.assertIsNone(cached)

    def test_sql_injection_safety(self):
        injection_intent = "test' OR '1'='1"
        response = '{"action": "none", "text": "safe"}'

        save_answer(injection_intent, response, db_path=self.db_path)

        # Should retrieve response for exact string match only
        self.assertEqual(
            get_cached_answer(injection_intent, db_path=self.db_path),
            response,
        )
        self.assertIsNone(
            get_cached_answer("test", db_path=self.db_path)
        )


if __name__ == "__main__":
    unittest.main()
