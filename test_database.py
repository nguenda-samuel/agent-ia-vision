import os
import tempfile
import unittest
import database


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_save_and_get_cached_answer(self):
        prompt = "How to click button?"
        answer = '{"action": "click", "x": 100, "y": 200, "text": "Clicking button"}'

        database.save_answer(prompt, answer, db_path=self.db_path)
        cached = database.get_cached_answer(prompt, db_path=self.db_path)

        self.assertEqual(cached, answer)

    def test_get_nonexistent_cached_answer(self):
        cached = database.get_cached_answer("Unknown prompt", db_path=self.db_path)
        self.assertIsNone(cached)

    def test_overwrite_cached_answer(self):
        prompt = "Same prompt"
        answer1 = '{"action": "none", "text": "First answer"}'
        answer2 = '{"action": "none", "text": "Updated answer"}'

        database.save_answer(prompt, answer1, db_path=self.db_path)
        database.save_answer(prompt, answer2, db_path=self.db_path)

        cached = database.get_cached_answer(prompt, db_path=self.db_path)
        self.assertEqual(cached, answer2)

    def test_sql_injection_prevention(self):
        # SQL injection payloads attempting bypass or table destruction
        sqli_prompts = [
            "' OR '1'='1",
            "'; DROP TABLE cache; --",
            "' UNION SELECT 1, 'hacked' --",
            "admin'--",
            "1' AND 1=1 --",
        ]

        for idx, sqli_prompt in enumerate(sqli_prompts):
            expected_answer = f'{{"action": "none", "text": "Safe response {idx}"}}'
            database.save_answer(sqli_prompt, expected_answer, db_path=self.db_path)
            cached = database.get_cached_answer(sqli_prompt, db_path=self.db_path)
            self.assertEqual(cached, expected_answer)

        # Verify cache table still exists and functions properly
        normal_prompt = "Normal test prompt"
        database.save_answer(normal_prompt, "OK", db_path=self.db_path)
        self.assertEqual(database.get_cached_answer(normal_prompt, db_path=self.db_path), "OK")


if __name__ == "__main__":
    unittest.main()
