import os
import unittest

os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["GEMINI_API_KEY"] = "dummy_key"

from main_vision import AvatarWindow, VisionAssistantApp


class TestMainVision(unittest.TestCase):

    def setUp(self):
        self.app = VisionAssistantApp()

    def tearDown(self):
        try:
            self.app.on_closing()
        except Exception:
            pass

    def test_button_states_during_processing(self):
        """Test that vision and send buttons are disabled during request processing and restored on stop."""
        self.assertEqual(self.app.btn_vision.cget("state"), "normal")
        self.assertEqual(self.app.btn_send.cget("state"), "normal")

        self.app.process_request(use_vision=False)

        self.assertEqual(self.app.btn_vision.cget("state"), "disabled")
        self.assertEqual(self.app.btn_send.cget("state"), "disabled")

        self.app.stop_agent_workflow()

        self.assertEqual(self.app.btn_vision.cget("state"), "normal")
        self.assertEqual(self.app.btn_send.cget("state"), "normal")

    def test_avatar_window_levitation(self):
        """Test that AvatarWindow creates fallback oval shape when avatar.png is missing and animates levitation without error."""
        avatar = AvatarWindow(self.app)
        self.assertFalse(getattr(avatar, "is_image_avatar", True))
        avatar.animate_ring_and_levitate()
        self.assertTrue(hasattr(avatar, "text_id"))


if __name__ == "__main__":
    unittest.main()
