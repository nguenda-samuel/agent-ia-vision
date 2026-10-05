import os
import unittest
from unittest.mock import MagicMock
import ai_engine
import database


class TestAIEngine(unittest.TestCase):

    def setUp(self):
        self.test_db = "cache.db"
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_cached_text_response_returned(self):
        mock_client = MagicMock()
        engine = ai_engine.AIEngine(mock_client)

        intent = "ouvrir le navigateur"
        cached_val = '{"action": "none", "text": "Le navigateur est ouvert"}'

        # Save cached answer in database
        database.save_answer(intent, cached_val)

        # Call process_screen_and_intent with no screenshot (text query)
        result = engine.process_screen_and_intent(
            raw_screenshot=None, user_intent=intent
        )

        self.assertEqual(result["text"], "Le navigateur est ouvert")


if __name__ == "__main__":
    unittest.main()
