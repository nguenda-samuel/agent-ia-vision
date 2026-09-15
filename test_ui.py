import os
import sys
from unittest.mock import MagicMock

# Mock database module before importing main_vision/ai_engine
sys.modules["database"] = MagicMock()

os.environ["SDL_AUDIODRIVER"] = "dummy"
if not os.environ.get("GEMINI_API_KEY"):
    os.environ["GEMINI_API_KEY"] = "fake_test_api_key"

import unittest
from main_vision import VisionAssistantApp


class TestButtonStateUX(unittest.TestCase):

    def setUp(self):
        self.app = VisionAssistantApp()

    def tearDown(self):
        self.app.on_closing()

    def test_buttons_disabled_during_processing_and_restored(self):
        # Initial state should be normal
        self.assertEqual(self.app.btn_send.cget("state"), "normal")
        self.assertEqual(self.app.btn_vision.cget("state"), "normal")
        self.assertEqual(self.app.quick_input.btn_send.cget("state"), "normal")
        self.assertEqual(self.app.quick_input.btn_vision.cget("state"), "normal")

        # Simulate process_request
        self.app.entry.insert(0, "Test prompt")
        self.app.process_request(use_vision=False)

        # Buttons should be disabled immediately
        self.assertEqual(self.app.btn_send.cget("state"), "disabled")
        self.assertEqual(self.app.btn_vision.cget("state"), "disabled")
        self.assertEqual(self.app.quick_input.btn_send.cget("state"), "disabled")
        self.assertEqual(self.app.quick_input.btn_vision.cget("state"), "disabled")

        # Stop workflow and verify state restoration
        self.app.stop_agent_workflow()
        self.assertEqual(self.app.btn_send.cget("state"), "normal")
        self.assertEqual(self.app.btn_vision.cget("state"), "normal")
        self.assertEqual(self.app.quick_input.btn_send.cget("state"), "normal")
        self.assertEqual(self.app.quick_input.btn_vision.cget("state"), "normal")


if __name__ == "__main__":
    unittest.main()
