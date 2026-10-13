import os
import tempfile
import unittest

from database import get_cached_answer, save_answer


class TestDatabaseSecurity(unittest.TestCase):

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_db.close()
        self.db_path = self.temp_db.name

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_save_and_get_cached_answer(self):
        intent = "ouvrir le navigateur"
        response = '{"action": "click", "x": 100, "y": 200, "text": "Ouverture"}'
        save_answer(intent, response, db_path=self.db_path)

        cached = get_cached_answer(intent, db_path=self.db_path)
        self.assertEqual(cached, response)

    def test_sql_injection_payload_handling(self):
        sqli_intent = "test' OR '1'='1"
        sqli_response = '{"action": "none", "text": "injection test"}'

        save_answer(sqli_intent, sqli_response, db_path=self.db_path)
        retrieved = get_cached_answer(sqli_intent, db_path=self.db_path)
        self.assertEqual(retrieved, sqli_response)

        # Confirm non-existent intent doesn't return anything
        other_intent = "other intent"
        self.assertIsNone(get_cached_answer(other_intent, db_path=self.db_path))


if __name__ == "__main__":
    unittest.main()
