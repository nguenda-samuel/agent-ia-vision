import json
import os
import sqlite3
import unittest
from memory import ActionMemory


class TestActionMemory(unittest.TestCase):

    def setUp(self):
        self.db_path = "test_memory.db"
        self.memory = ActionMemory(db_path=self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_save_and_get_routine(self):
        data = {"action": "click", "x": 100, "y": 200}
        self.memory.save_routine("hash123", "click submit", data)
        result = self.memory.get_routine("hash123", "click submit")
        self.assertEqual(result, data)

    def test_get_nonexistent_routine(self):
        result = self.memory.get_routine("nonexistent_hash", "nonexistent_intent")
        self.assertIsNone(result)

    def test_index_created(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='index' AND name='idx_routines_hash_intent'"
            )
            result = cursor.fetchone()
            self.assertIsNotNone(result)
            self.assertEqual(result[0], "idx_routines_hash_intent")


if __name__ == "__main__":
    unittest.main()
