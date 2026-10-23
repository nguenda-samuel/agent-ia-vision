import os
import tempfile
import unittest
from memory import ActionMemory


class TestActionMemorySecurity(unittest.TestCase):

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db.close()
        self.memory = ActionMemory(db_path=self.temp_db.name)

    def tearDown(self):
        if os.path.exists(self.temp_db.name):
            os.remove(self.temp_db.name)

    def test_sql_injection_safety_in_save_and_get(self):
        sql_injection_hash = "' OR '1'='1"
        sql_injection_intent = "'; DROP TABLE routines; --"
        action_data = {"action": "click", "x": 100, "y": 200}

        # Save routine with potential SQL injection payload
        self.memory.save_routine(
            sql_injection_hash, sql_injection_intent, action_data
        )

        # Retrieve routine using the exact payload
        result = self.memory.get_routine(
            sql_injection_hash, sql_injection_intent
        )

        self.assertIsNotNone(result)
        self.assertEqual(result, action_data)

        # Query with non-matching intent should return None, proving query structure intact
        result_other = self.memory.get_routine(
            sql_injection_hash, "normal_intent"
        )
        self.assertIsNone(result_other)


if __name__ == "__main__":
    unittest.main()
