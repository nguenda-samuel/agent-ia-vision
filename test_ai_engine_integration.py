import sys
from unittest.mock import MagicMock

# Mock dependencies not installed in the lightweight test environment
for mod in ["google", "google.genai", "google.genai.types", "cv2", "PIL", "imagehash", "privacy", "stream"]:
    if mod not in sys.modules:
        sys.modules[mod] = MagicMock()

import os
import unittest
import database

TEST_DB_PATH = "test_ai_cache.db"

class TestAIEngineDatabaseIntegration(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)

    def tearDown(self):
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)

    def test_ai_engine_cache_lookup(self):
        database.save_answer("test_intent", '{"action": "none", "text": "cached"}', db_path=TEST_DB_PATH)

        import ai_engine
        engine = ai_engine.AIEngine(gemini_client=MagicMock())

        # Mock database.get_cached_answer inside ai_engine to use TEST_DB_PATH
        original_get_cached = ai_engine.get_cached_answer
        ai_engine.get_cached_answer = lambda intent: database.get_cached_answer(intent, db_path=TEST_DB_PATH)
        try:
            result = engine.process_screen_and_intent(raw_screenshot=None, user_intent="test_intent")
            self.assertEqual(result, {"action": "none", "text": "cached"})
        finally:
            ai_engine.get_cached_answer = original_get_cached

if __name__ == "__main__":
    unittest.main()
