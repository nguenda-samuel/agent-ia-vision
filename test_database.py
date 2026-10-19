import os
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
        intent = "Open Settings"
        response = '{"action": "click", "x": 100, "y": 200, "text": "Clicking settings"}'
        save_answer(intent, response, db_path=self.db_path)

        cached = get_cached_answer(intent, db_path=self.db_path)
        self.assertEqual(cached, response)

    def test_get_nonexistent_answer(self):
        cached = get_cached_answer("Nonexistent intent", db_path=self.db_path)
        self.assertIsNone(cached)

    def test_update_cached_answer(self):
        intent = "Open Settings"
        response1 = '{"action": "wait", "text": "Waiting"}'
        response2 = '{"action": "click", "x": 50, "y": 50, "text": "Clicking"}'

        save_answer(intent, response1, db_path=self.db_path)
        save_answer(intent, response2, db_path=self.db_path)

        cached = get_cached_answer(intent, db_path=self.db_path)
        self.assertEqual(cached, response2)

    def test_sql_injection_prevention(self):
        # Payload that would compromise unparameterized query
        sql_injection_intent = "test' OR '1'='1"
        sql_injection_response = "'; DROP TABLE cache; --"

        save_answer(
            sql_injection_intent,
            sql_injection_response,
            db_path=self.db_path,
        )

        # Confirm exact string match and that table was not dropped
        cached = get_cached_answer(sql_injection_intent, db_path=self.db_path)
        self.assertEqual(cached, sql_injection_response)

        # Confirm normal queries still work
        normal_intent = "Normal intent"
        save_answer(normal_intent, "Normal response", db_path=self.db_path)
        self.assertEqual(
            get_cached_answer(normal_intent, db_path=self.db_path),
            "Normal response",
        )


if __name__ == "__main__":
    unittest.main()
