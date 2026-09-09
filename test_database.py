import os
import tempfile
import unittest

import database


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_get_cached_answer_returns_none_for_missing_intent(self):
        result = database.get_cached_answer(
            "non_existent_intent", db_path=self.db_path
        )
        self.assertIsNone(result)

    def test_save_and_get_cached_answer(self):
        intent = "Open music player"
        answer = (
            '{"action": "click", "x": 100, "y": 200, "text": "Opening music'
            ' player"}'
        )
        database.save_answer(intent, answer, db_path=self.db_path)

        cached = database.get_cached_answer(intent, db_path=self.db_path)
        self.assertEqual(cached, answer)

    def test_sql_injection_prevention(self):
        malicious_intent = "Open music'; DROP TABLE answer_cache; --"
        answer = '{"action": "none", "text": "safe"}'
        database.save_answer(malicious_intent, answer, db_path=self.db_path)

        cached = database.get_cached_answer(
            malicious_intent, db_path=self.db_path
        )
        self.assertEqual(cached, answer)

        # Verify table structure is intact and table was not dropped
        normal_intent = "Normal intent"
        database.save_answer(
            normal_intent, "normal_answer", db_path=self.db_path
        )
        self.assertEqual(
            database.get_cached_answer(normal_intent, db_path=self.db_path),
            "normal_answer",
        )


if __name__ == "__main__":
    unittest.main()
