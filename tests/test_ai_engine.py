import sys
import unittest
from unittest.mock import MagicMock

# Mock database module before importing ai_engine
mock_db = MagicMock()
mock_db.get_cached_answer.return_value = None
sys.modules["database"] = mock_db

from PIL import Image
import numpy as np
from ai_engine import AIEngine


class TestAIEngine(unittest.TestCase):

    def setUp(self):
        self.mock_client = MagicMock()
        self.engine = AIEngine(gemini_client=self.mock_client)

    def test_process_screen_and_intent_no_screenshot(self):
        # When no screenshot provided and no cache, returns warning message
        result = self.engine.process_screen_and_intent(None, "test intent")
        self.assertIn("action", result)
        self.assertEqual(result["action"], "none")

    def test_process_screen_and_intent_vision(self):
        img = Image.fromarray(np.zeros((100, 100, 3), dtype=np.uint8))
        mock_response = MagicMock()
        mock_response.text = '{"action": "click", "x": 50, "y": 50, "text": "Clicked button"}'
        self.mock_client.models.generate_content.return_value = mock_response

        result = self.engine.process_screen_and_intent(img, "test vision intent")
        self.assertEqual(result["action"], "click")
        self.assertEqual(result["x"], 50)


if __name__ == "__main__":
    unittest.main()
