import unittest
from unittest.mock import MagicMock
import numpy as np
from PIL import Image

import database
from privacy import PrivacyFilter
from stream import ScreenStream
from ai_engine import AIEngine


class TestDatabase(unittest.TestCase):

    def test_save_and_get_cached_answer(self):
        intent = "test_intent_123"
        answer = '{"action": "none", "text": "cached test answer"}'
        database.save_answer(intent, answer)

        cached = database.get_cached_answer(intent)
        self.assertEqual(cached, answer)

    def test_get_nonexistent_cached_answer(self):
        cached = database.get_cached_answer("non_existent_intent_99999")
        self.assertIsNone(cached)


class TestScreenStream(unittest.TestCase):

    def setUp(self):
        self.stream = ScreenStream(threshold=5)

    def test_has_screen_changed(self):
        img1 = Image.fromarray(np.zeros((100, 100, 3), dtype=np.uint8))

        # Create a distinct patterned image
        np.random.seed(42)
        arr2 = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
        img2 = Image.fromarray(arr2)

        # First frame should return True
        self.assertTrue(self.stream.has_screen_changed(img1))
        # Same image frame should return False
        self.assertFalse(self.stream.has_screen_changed(img1))
        # Structurally different image frame should return True
        self.assertTrue(self.stream.has_screen_changed(img2))

    def test_wait_until_stable(self):
        img = Image.fromarray(np.zeros((100, 100, 3), dtype=np.uint8))
        capture_func = MagicMock(return_value=img)

        result = self.stream.wait_until_stable(
            capture_func, poll_interval=0.01, max_wait=0.1
        )
        self.assertIsNotNone(result)
        self.assertTrue(capture_func.call_count >= 1)


class TestPrivacyFilter(unittest.TestCase):

    def test_redact_sensitive_data(self):
        pf = PrivacyFilter()
        img_array = np.full((200, 200, 3), 128, dtype=np.uint8)
        pil_img = Image.fromarray(img_array)

        redacted = pf.redact_sensitive_data(pil_img)
        self.assertEqual(redacted.size, (200, 200))
        self.assertEqual(redacted.mode, "RGB")


class TestAIEngine(unittest.TestCase):

    def test_cached_text_response(self):
        mock_client = MagicMock()
        ai = AIEngine(gemini_client=mock_client)

        database.save_answer("pure_text_intent", '{"action": "none", "text": "OK"}')
        result = ai.process_screen_and_intent(None, "pure_text_intent")

        self.assertEqual(result.get("text"), "OK")
        self.assertEqual(result.get("action"), "none")

    def test_no_screenshot_and_no_cache(self):
        mock_client = MagicMock()
        ai = AIEngine(gemini_client=mock_client)

        result = ai.process_screen_and_intent(None, "random_uncached_intent_12345")
        self.assertEqual(result.get("action"), "none")
        self.assertIn("Désolé", result.get("text"))


if __name__ == "__main__":
    unittest.main()
