import os
import tempfile
import unittest

from database import get_cached_answer, save_answer


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        self.temp_db_fd, self.temp_db_path = tempfile.mkstemp(suffix=".db")
        os.close(self.temp_db_fd)

    def tearDown(self):
        if os.path.exists(self.temp_db_path):
            os.remove(self.temp_db_path)

    def test_save_and_get_cached_answer(self):
        intent = "ouvrir le navigateur"
        response = '{"action": "click", "x": 100, "y": 200, "text": "Ouverture"}'

        # Initially not in cache
        self.assertIsNone(get_cached_answer(intent, db_path=self.temp_db_path))

        # Save to cache
        save_answer(intent, response, db_path=self.temp_db_path)

        # Retrieve from cache
        cached = get_cached_answer(intent, db_path=self.temp_db_path)
        self.assertEqual(cached, response)

    def test_update_cached_answer_on_conflict(self):
        intent = "ouvrir les paramètres"
        response_v1 = '{"action": "none", "text": "V1"}'
        response_v2 = '{"action": "none", "text": "V2"}'

        save_answer(intent, response_v1, db_path=self.temp_db_path)
        self.assertEqual(
            get_cached_answer(intent, db_path=self.temp_db_path), response_v1
        )

        save_answer(intent, response_v2, db_path=self.temp_db_path)
        self.assertEqual(
            get_cached_answer(intent, db_path=self.temp_db_path), response_v2
        )

    def test_sql_injection_defense(self):
        # Injection attempts should be treated strictly as literal values and not execute SQL
        sql_injection_payload = "test' OR '1'='1"
        response = '{"action": "none", "text": "Safe"}'

        save_answer(sql_injection_payload, response, db_path=self.temp_db_path)

        # Searching for another intent should return None, not the injected entry
        self.assertIsNone(
            get_cached_answer("another intent", db_path=self.temp_db_path)
        )

        # Exact match of the payload returns the stored response
        self.assertEqual(
            get_cached_answer(sql_injection_payload, db_path=self.temp_db_path),
            response,
        )

        # Test another injection payload that attempts DROP TABLE
        drop_payload = "intent'; DROP TABLE answer_cache; --"
        save_answer(drop_payload, response, db_path=self.temp_db_path)
        # Verify table still exists and answers are retrievable
        self.assertEqual(
            get_cached_answer(drop_payload, db_path=self.temp_db_path),
            response,
        )


if __name__ == "__main__":
    unittest.main()
