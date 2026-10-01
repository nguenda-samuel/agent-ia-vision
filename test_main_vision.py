import os
import unittest

os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["GEMINI_API_KEY"] = "dummy"

from main_vision import VisionAssistantApp


class TestVisionAssistantAppUX(unittest.TestCase):

    def setUp(self):
        self.app = VisionAssistantApp()

    def tearDown(self):
        self.app.destroy()

    def test_initial_button_states(self):
        self.assertFalse(self.app.is_processing)
        self.assertEqual(self.app.btn_send.cget("state"), "normal")
        self.assertEqual(self.app.btn_vision.cget("state"), "normal")

    def test_set_processing_state_disables_and_enables_buttons(self):
        # Set processing to True -> buttons should be disabled
        self.app.set_processing_state(True)
        self.assertTrue(self.app.is_processing)
        self.assertEqual(self.app.btn_send.cget("state"), "disabled")
        self.assertEqual(self.app.btn_vision.cget("state"), "disabled")

        # Set processing to False -> buttons should be re-enabled
        self.app.set_processing_state(False)
        self.assertFalse(self.app.is_processing)
        self.assertEqual(self.app.btn_send.cget("state"), "normal")
        self.assertEqual(self.app.btn_vision.cget("state"), "normal")

    def test_stop_agent_workflow_re_enables_buttons(self):
        self.app.set_processing_state(True)
        self.assertEqual(self.app.btn_send.cget("state"), "disabled")

        self.app.stop_agent_workflow()
        self.assertFalse(self.app.is_processing)
        self.assertEqual(self.app.btn_send.cget("state"), "normal")
        self.assertEqual(self.app.btn_vision.cget("state"), "normal")


if __name__ == "__main__":
    unittest.main()
