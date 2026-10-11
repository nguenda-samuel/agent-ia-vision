import os
import unittest

# Ensure dummy environment variables for headless testing
os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["GEMINI_API_KEY"] = "dummy"

from main_vision import VisionAssistantApp


class TestVisionAssistantAppUI(unittest.TestCase):

    def setUp(self):
        self.app = VisionAssistantApp()

    def tearDown(self):
        self.app.on_closing()

    def test_set_buttons_state_disabled_and_normal(self):
        """Verify set_buttons_state correctly updates btn_vision and btn_send states."""
        self.app.set_buttons_state("disabled")
        self.assertEqual(self.app.btn_vision.cget("state"), "disabled")
        self.assertEqual(self.app.btn_send.cget("state"), "disabled")

        self.app.set_buttons_state("normal")
        self.assertEqual(self.app.btn_vision.cget("state"), "normal")
        self.assertEqual(self.app.btn_send.cget("state"), "normal")

    def test_stop_agent_workflow_resets_buttons_state(self):
        """Verify stop_agent_workflow sets buttons back to normal state."""
        self.app.set_buttons_state("disabled")
        self.app.stop_agent_workflow()
        self.assertEqual(self.app.btn_vision.cget("state"), "normal")
        self.assertEqual(self.app.btn_send.cget("state"), "normal")


if __name__ == "__main__":
    unittest.main()
