import os
import unittest
import tempfile
from memory import ActionMemory
from database import get_cached_answer, save_answer


class TestActionMemory(unittest.TestCase):

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_db.close()
        self.memory = ActionMemory(db_path=self.temp_db.name)

    def tearDown(self):
        if os.path.exists(self.temp_db.name):
            os.remove(self.temp_db.name)

    def test_save_and_get_routine(self):
        screen_hash = "hash_12345"
        user_intent = "click on button"
        action_data = {"action": "click", "x": 100, "y": 200}

        self.memory.save_routine(screen_hash, user_intent, action_data)
        result = self.memory.get_routine(screen_hash, user_intent)

        self.assertEqual(result, action_data)

    def test_get_nonexistent_routine(self):
        result = self.memory.get_routine("nonexistent_hash", "nonexistent_intent")
        self.assertIsNone(result)

    def test_sql_injection_resilience(self):
        malicious_intent = "click' OR '1'='1"
        malicious_hash = "hash'; DROP TABLE routines; --"
        action_data = {"action": "safe"}

        self.memory.save_routine(malicious_hash, malicious_intent, action_data)
        result = self.memory.get_routine(malicious_hash, malicious_intent)

        self.assertEqual(result, action_data)

    def test_database_cache_functions(self):
        intent = "What is the weather?"
        answer = '{"action": "none", "text": "It is sunny."}'

        save_answer(intent, answer, db_path=self.temp_db.name)
        cached = get_cached_answer(intent, db_path=self.temp_db.name)

        self.assertEqual(cached, answer)


if __name__ == "__main__":
    unittest.main()
