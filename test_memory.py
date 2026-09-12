import os
import sqlite3
import tempfile
import unittest

from memory import ActionMemory


class TestActionMemory(unittest.TestCase):

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db.close()
        self.memory = ActionMemory(db_path=self.temp_db.name)

    def tearDown(self):
        if os.path.exists(self.temp_db.name):
            os.remove(self.temp_db.name)

    def test_index_created(self):
        with sqlite3.connect(self.temp_db.name) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA index_list(routines)")
            indexes = [row[1] for row in cursor.fetchall()]
            self.assertIn("idx_routines_hash_intent", indexes)

    def test_save_and_get_routine(self):
        screen_hash = "abc123hash"
        intent = "click play button"
        action = {"action": "click", "x": 100, "y": 200}

        self.assertIsNone(self.memory.get_routine(screen_hash, intent))

        self.memory.save_routine(screen_hash, intent, action)
        retrieved = self.memory.get_routine(screen_hash, intent)

        self.assertEqual(retrieved, action)


if __name__ == "__main__":
    unittest.main()
