import os
import unittest

os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["GEMINI_API_KEY"] = "dummy_key"

from main_vision import ToolTip, VisionAssistantApp


class TestUIImprovements(unittest.TestCase):

    def setUp(self):
        self.app = VisionAssistantApp()

    def tearDown(self):
        self.app.destroy()

    def test_button_processing_state_toggle(self):
        """Tests that _set_processing_state updates button states across main and quick input windows."""
        self.assertFalse(self.app.is_processing)
        self.assertEqual(self.app.btn_vision.cget("state"), "normal")
        self.assertEqual(self.app.btn_send.cget("state"), "normal")
        self.assertEqual(self.app.quick_input.btn_vision.cget("state"), "normal")
        self.assertEqual(self.app.quick_input.btn_send.cget("state"), "normal")

        # Set processing state to True
        self.app._set_processing_state(True)
        self.assertTrue(self.app.is_processing)
        self.assertEqual(self.app.btn_vision.cget("state"), "disabled")
        self.assertEqual(self.app.btn_send.cget("state"), "disabled")
        self.assertEqual(self.app.quick_input.btn_vision.cget("state"), "disabled")
        self.assertEqual(self.app.quick_input.btn_send.cget("state"), "disabled")

        # Reset processing state to False
        self.app._set_processing_state(False)
        self.assertFalse(self.app.is_processing)
        self.assertEqual(self.app.btn_vision.cget("state"), "normal")
        self.assertEqual(self.app.btn_send.cget("state"), "normal")
        self.assertEqual(self.app.quick_input.btn_vision.cget("state"), "normal")
        self.assertEqual(self.app.quick_input.btn_send.cget("state"), "normal")

    def test_tooltip_show_and_hide(self):
        """Tests that ToolTip displays and destroys tooltip windows on enter and leave events."""
        tooltip = ToolTip(self.app.btn_vision, "Test Tooltip")
        self.assertIsNone(tooltip.tip_window)

        # Trigger hover enter
        tooltip.show_tooltip()
        self.assertIsNotNone(tooltip.tip_window)

        # Trigger hover leave
        tooltip.hide_tooltip()
        self.assertIsNone(tooltip.tip_window)

    def test_avatar_levitation_animation_fallback(self):
        """Tests that AvatarWindow levitation animation runs smoothly without errors when avatar image is missing."""
        avatar = self.app.avatar
        self.assertIsNotNone(avatar)
        # Force one cycle of animate_ring_and_levitate
        avatar.animate_ring_and_levitate()


if __name__ == "__main__":
    unittest.main()
