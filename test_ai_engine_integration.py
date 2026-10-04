import os
import sys
import unittest
from unittest.mock import MagicMock

# Mock third-party dependencies if not present in test environment
for mod in ["google", "google.genai", "google.genai.types", "cv2", "imagehash", "numpy", "PIL"]:
    if mod not in sys.modules:
        sys.modules[mod] = MagicMock()

import database
from ai_engine import AIEngine

TEST_DB_PATH = "test_ai_engine_cache.db"


class TestAIEngineDatabaseIntegration(unittest.TestCase):

    def setUp(self):
        self.original_db_path = database.DB_PATH
        database.DB_PATH = TEST_DB_PATH
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)

    def tearDown(self):
        database.DB_PATH = self.original_db_path
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)

    def test_text_only_intent_uses_database_cache(self):
        mock_gemini = MagicMock()
        ai = AIEngine(gemini_client=mock_gemini)

        # Pre-seed cache in database using parameterized query function
        database.save_answer("hello assistant", '{"action": "none", "text": "Hello user!"}', db_path=TEST_DB_PATH)

        # Execute text-only intent (raw_screenshot=None)
        result = ai.process_screen_and_intent(raw_screenshot=None, user_intent="hello assistant")

        # Verify cached response returned and gemini client was never called
        self.assertEqual(result, {"action": "none", "text": "Hello user!"})
        mock_gemini.models.generate_content.assert_not_called()


if __name__ == "__main__":
    unittest.main()
