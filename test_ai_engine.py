import json
import os
import tempfile
import unittest
from unittest.mock import MagicMock

# Set dummy key for tests before importing modules that might expect it
os.environ["GEMINI_API_KEY"] = "dummy_key"

import database
from ai_engine import AIEngine


class TestAIEngineCaching(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.original_db_path = database.DB_PATH
        database.DB_PATH = self.db_path

    def tearDown(self):
        database.DB_PATH = self.original_db_path
        os.close(self.db_fd)
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_text_only_query_uses_database_cache(self):
        mock_client = MagicMock()
        engine = AIEngine(gemini_client=mock_client)

        intent = "What time is it?"
        expected_response = {"action": "none", "text": "It is 12:00 PM"}

        # Save cached answer in database
        database.save_answer(intent, json.dumps(expected_response))

        # Call process_screen_and_intent without screenshot
        result = engine.process_screen_and_intent(
            raw_screenshot=None, user_intent=intent
        )

        # Confirm cached response is returned without calling Gemini client
        self.assertEqual(result, expected_response)
        mock_client.models.generate_content.assert_not_called()


if __name__ == "__main__":
    unittest.main()
