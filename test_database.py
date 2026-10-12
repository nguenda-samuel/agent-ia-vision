import os
import tempfile
import unittest
from database import get_cached_answer, save_answer


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_db.close()

    def tearDown(self):
        if os.path.exists(self.temp_db.name):
            os.remove(self.temp_db.name)

    def test_save_and_get_cached_answer(self):
        intent = "Open settings menu"
        answer = '{"action": "click", "x": 50, "y": 50, "text": "Opening settings"}'

        save_answer(intent, answer, db_path=self.temp_db.name)
        cached = get_cached_answer(intent, db_path=self.temp_db.name)

        self.assertEqual(cached, answer)

    def test_get_nonexistent_cache(self):
        cached = get_cached_answer("nonexistent intent", db_path=self.temp_db.name)
        self.assertIsNone(cached)

    test_sql_injection_intent = "Open ';' DROP TABLE cache; --"

    def test_sql_injection_prevention(self):
        intent = self.test_sql_injection_intent
        answer = "Safe answer"

        save_answer(intent, answer, db_path=self.temp_db.name)
        cached = get_cached_answer(intent, db_path=self.temp_db.name)

        self.assertEqual(cached, answer)


if __name__ == "__main__":
    unittest.main()
