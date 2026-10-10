import os
import tempfile
import unittest
import database


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")
        os.close(self.db_fd)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_save_and_get_cached_answer(self):
        intent = "Open settings"
        response = '{"action": "click", "x": 10, "y": 20}'

        database.save_answer(intent, response, db_path=self.db_path)
        cached = database.get_cached_answer(intent, db_path=self.db_path)

        self.assertEqual(cached, response)

    def test_update_existing_cache(self):
        intent = "Open settings"
        response1 = '{"action": "none"}'
        response2 = '{"action": "click", "x": 100, "y": 200}'

        database.save_answer(intent, response1, db_path=self.db_path)
        database.save_answer(intent, response2, db_path=self.db_path)
        cached = database.get_cached_answer(intent, db_path=self.db_path)

        self.assertEqual(cached, response2)

    def test_sql_injection_prevention(self):
        malicious_intent = "' OR '1'='1'; DROP TABLE answer_cache; --"
        malicious_response = "injected_data"

        database.save_answer(malicious_intent, malicious_response, db_path=self.db_path)
        cached = database.get_cached_answer(malicious_intent, db_path=self.db_path)

        self.assertEqual(cached, malicious_response)

        # Verify table answer_cache still exists and other entries are safe
        normal_cached = database.get_cached_answer("non_existent_intent", db_path=self.db_path)
        self.assertIsNone(normal_cached)


if __name__ == "__main__":
    unittest.main()
