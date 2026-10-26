import os
import sys
import types
import unittest

# Ensure dummy env vars before importing main_vision
os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["GEMINI_API_KEY"] = "dummy_key"

# Mock database module if not present
if "database" not in sys.modules:
    db_mock = types.ModuleType("database")
    db_mock.get_cached_answer = lambda k: None
    db_mock.save_answer = lambda k, v: None
    sys.modules["database"] = db_mock

import main_vision


class TestAppUX(unittest.TestCase):

    def setUp(self):
        self.app = main_vision.VisionAssistantApp()

    def tearDown(self):
        self.app.destroy()

    def test_button_states_toggle(self):
        """Verify that action buttons can be disabled and re-enabled."""
        self.assertEqual(self.app.btn_vision.cget("state"), "normal")
        self.assertEqual(self.app.btn_send.cget("state"), "normal")
        self.assertEqual(self.app.quick_input.btn_vision.cget("state"), "normal")
        self.assertEqual(self.app.quick_input.btn_send.cget("state"), "normal")

        self.app.set_button_states("disabled")
        self.assertEqual(self.app.btn_vision.cget("state"), "disabled")
        self.assertEqual(self.app.btn_send.cget("state"), "disabled")
        self.assertEqual(self.app.quick_input.btn_vision.cget("state"), "disabled")
        self.assertEqual(self.app.quick_input.btn_send.cget("state"), "disabled")

        self.app.set_button_states("normal")
        self.assertEqual(self.app.btn_vision.cget("state"), "normal")

    def test_stop_agent_workflow_resets_buttons(self):
        """Verify that stopping agent workflow resets buttons to normal state."""
        self.app.set_button_states("disabled")
        self.app.stop_agent_workflow()
        self.assertEqual(self.app.btn_vision.cget("state"), "normal")
        self.assertEqual(self.app.btn_send.cget("state"), "normal")


if __name__ == "__main__":
    unittest.main()
