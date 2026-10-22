import os
import sys
import unittest
from unittest.mock import MagicMock

# Environment mocks for GUI and API
os.environ["GEMINI_API_KEY"] = "dummy_api_key"
os.environ["SDL_AUDIODRIVER"] = "dummy"

# Mock database module if not present
if "database" not in sys.modules:
    mock_db = MagicMock()
    mock_db.get_cached_answer.return_value = None
    mock_db.save_answer = MagicMock()
    sys.modules["database"] = mock_db

from main_vision import VisionAssistantApp


class TestUIState(unittest.TestCase):

    def setUp(self):
        self.app = VisionAssistantApp()

    def tearDown(self):
        self.app.destroy()

    def test_set_input_state_disabled_and_normal(self):
        # Verify initial button states
        self.assertEqual(self.app.btn_vision.cget("state"), "normal")
        self.assertEqual(self.app.btn_send.cget("state"), "normal")
        self.assertEqual(self.app.quick_input.btn_vision.cget("state"), "normal")
        self.assertEqual(self.app.quick_input.btn_send.cget("state"), "normal")

        # Disable input controls
        self.app.set_input_state("disabled")
        self.assertEqual(self.app.btn_vision.cget("state"), "disabled")
        self.assertEqual(self.app.btn_send.cget("state"), "disabled")
        self.assertEqual(self.app.quick_input.btn_vision.cget("state"), "disabled")
        self.assertEqual(self.app.quick_input.btn_send.cget("state"), "disabled")

        # Restore input controls to normal
        self.app.set_input_state("normal")
        self.assertEqual(self.app.btn_vision.cget("state"), "normal")
        self.assertEqual(self.app.btn_send.cget("state"), "normal")
        self.assertEqual(self.app.quick_input.btn_vision.cget("state"), "normal")
        self.assertEqual(self.app.quick_input.btn_send.cget("state"), "normal")


if __name__ == "__main__":
    unittest.main()
