import os
import unittest
from unittest.mock import MagicMock, patch

# Set required dummy env vars for headless environment
os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["GEMINI_API_KEY"] = "dummy"

import main_vision


class TestAppUX(unittest.TestCase):

    def setUp(self):
        self.app = main_vision.VisionAssistantApp()

    def tearDown(self):
        self.app.destroy()

    def test_initial_button_states(self):
        """Verify buttons start in normal active state."""
        self.assertEqual(self.app.btn_send.cget("state"), "normal")
        self.assertEqual(self.app.btn_send.cget("text"), "🚀")
        self.assertEqual(self.app.btn_vision.cget("state"), "normal")

    def test_set_inputs_state_loading(self):
        """Verify buttons transition to disabled state with loading indicator."""
        self.app._set_inputs_state(True)
        self.assertEqual(self.app.btn_send.cget("state"), "disabled")
        self.assertEqual(self.app.btn_send.cget("text"), "⏳")
        self.assertEqual(self.app.btn_vision.cget("state"), "disabled")

    def test_set_inputs_state_reset(self):
        """Verify buttons reset to normal state."""
        self.app._set_inputs_state(True)
        self.app._set_inputs_state(False)
        self.assertEqual(self.app.btn_send.cget("state"), "normal")
        self.assertEqual(self.app.btn_send.cget("text"), "🚀")
        self.assertEqual(self.app.btn_vision.cget("state"), "normal")

    def test_stop_agent_workflow_resets_inputs(self):
        """Verify stopping workflow re-enables input buttons."""
        self.app._set_inputs_state(True)
        self.app.stop_agent_workflow()
        self.assertEqual(self.app.btn_send.cget("state"), "normal")
        self.assertEqual(self.app.btn_send.cget("text"), "🚀")
        self.assertEqual(self.app.btn_vision.cget("state"), "normal")


if __name__ == "__main__":
    unittest.main()
