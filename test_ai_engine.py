import unittest
from unittest.mock import MagicMock, patch
from PIL import Image
import numpy as np

import os
os.environ["GEMINI_API_KEY"] = "dummy_key_for_testing"

# Mock database module before importing ai_engine
import sys
mock_db = MagicMock()
mock_db.get_cached_answer.return_value = None
mock_db.save_answer = MagicMock()
sys.modules["database"] = mock_db

from ai_engine import AIEngine


class TestAIEngine(unittest.TestCase):

    def setUp(self):
        self.mock_client = MagicMock()
        self.engine = AIEngine(gemini_client=self.mock_client)

    def test_no_screenshot(self):
        mock_db.get_cached_answer.return_value = None
        result = self.engine.process_screen_and_intent(None, "Test intent")
        self.assertEqual(result["action"], "none")
        self.assertIn("Désolé", result["text"])

    def test_process_screen_and_intent_downscaling(self):
        mock_db.get_cached_answer.return_value = None

        # Mock Gemini response
        mock_response = MagicMock()
        mock_response.text = '{"action": "click", "x": 500, "y": 500, "text": "Clique ici"}'
        self.mock_client.models.generate_content.return_value = mock_response

        # Create large image (1920x1080)
        large_image = Image.fromarray(np.zeros((1080, 1920, 3), dtype=np.uint8))

        with patch.object(self.engine.privacy, "redact_sensitive_data", wraps=self.engine.privacy.redact_sensitive_data) as mock_redact:
            res = self.engine.process_screen_and_intent(large_image, "Clique sur le bouton")

            self.assertEqual(res["action"], "click")
            mock_redact.assert_called_once()

            # Verify the image passed to redact_sensitive_data was downscaled (max dim 768)
            passed_img = mock_redact.call_args[0][0]
            self.assertLessEqual(passed_img.width, 768)
            self.assertLessEqual(passed_img.height, 768)


if __name__ == "__main__":
    unittest.main()
