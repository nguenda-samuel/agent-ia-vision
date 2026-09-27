import os
import sqlite3
import tempfile
import unittest
from memory import ActionMemory


class TestActionMemorySecurity(unittest.TestCase):

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_db.close()
        self.memory = ActionMemory(db_path=self.temp_db.name)

    def tearDown(self):
        if os.path.exists(self.temp_db.name):
            os.remove(self.temp_db.name)

    def test_save_and_get_routine_normal(self):
        hash_val = "hash123"
        intent = "click button"
        action = {"action": "click", "x": 100, "y": 200}

        self.memory.save_routine(hash_val, intent, action)
        res = self.memory.get_routine(hash_val, intent)
        self.assertEqual(res, action)

    def test_sql_injection_in_user_intent(self):
        hash_val = "hash123"
        sql_injection_payload = "' OR '1'='1"
        action = {"action": "click", "x": 50, "y": 50}

        # Save routine with SQL injection payload as intent
        self.memory.save_routine(hash_val, sql_injection_payload, action)

        # Searching for a different intent should NOT match via injection
        res_empty = self.memory.get_routine(hash_val, "click button")
        self.assertIsNone(res_empty)

        # Searching for exact payload should match safely
        res_exact = self.memory.get_routine(hash_val, sql_injection_payload)
        self.assertEqual(res_exact, action)

    def test_sql_injection_drop_table(self):
        hash_val = "hash123"
        drop_payload = "test'; DROP TABLE routines; --"
        action = {"action": "none"}

        self.memory.save_routine(hash_val, drop_payload, action)
        res = self.memory.get_routine(hash_val, drop_payload)
        self.assertEqual(res, action)

        # Check table still exists
        with sqlite3.connect(self.temp_db.name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT count(*) FROM routines")
            count = cursor.fetchone()[0]
            self.assertGreaterEqual(count, 1)


if __name__ == "__main__":
    unittest.main()
