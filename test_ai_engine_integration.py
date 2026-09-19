import sys
from unittest.mock import MagicMock

# Mock missing modules if not installed in sandbox environment
for module_name in ["google", "google.genai", "google.genai.types", "cv2", "mss", "pygame", "PIL", "imagehash", "numpy"]:
    if module_name not in sys.modules:
        sys.modules[module_name] = MagicMock()

import os
import unittest

from ai_engine import AIEngine
from database import get_cached_answer, save_answer


class TestAIEngineIntegration(unittest.TestCase):

    def setUp(self):
        if os.path.exists("cache.db"):
            os.remove("cache.db")

    def tearDown(self):
        if os.path.exists("cache.db"):
            os.remove("cache.db")

    def test_ai_engine_uses_database_cache(self):
        mock_client = MagicMock()
        ai_engine = AIEngine(gemini_client=mock_client)

        user_intent = "Test intent"
        cached_data = '{"action": "none", "text": "Cached response"}'

        # Save cached answer into DB
        save_answer(user_intent, cached_data)

        # Without raw_screenshot, process_screen_and_intent should return cached answer
        res = ai_engine.process_screen_and_intent(None, user_intent)
        self.assertEqual(res, {"action": "none", "text": "Cached response"})


if __name__ == "__main__":
    unittest.main()
