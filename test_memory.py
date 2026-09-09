import os
import unittest
from memory import ActionMemory


class TestActionMemory(unittest.TestCase):

    def setUp(self):
        self.db_file = "test_memory_db.db"
        if os.path.exists(self.db_file):
            os.remove(self.db_file)
        self.mem = ActionMemory(self.db_file)

    def tearDown(self):
        if os.path.exists(self.db_file):
            os.remove(self.db_file)

    def test_save_and_get_routine(self):
        action_data = {
            "action": "click",
            "x": 100,
            "y": 200,
            "text": "Click button",
        }
        self.mem.save_routine("hash1", "intent1", action_data)

        res = self.mem.get_routine("hash1", "intent1")
        self.assertEqual(res, action_data)

        res_none = self.mem.get_routine("hash2", "intent1")
        self.assertIsNone(res_none)

    def test_latest_routine_returned(self):
        action1 = {"action": "click", "x": 10}
        action2 = {"action": "click", "x": 20}
        self.mem.save_routine("hash1", "intent1", action1)
        self.mem.save_routine("hash1", "intent1", action2)

        res = self.mem.get_routine("hash1", "intent1")
        self.assertEqual(res, action2)


if __name__ == "__main__":
    unittest.main()
