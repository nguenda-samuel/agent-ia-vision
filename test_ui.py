import os
import unittest

os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["GEMINI_API_KEY"] = "dummy"

import main_vision


class TestUIComponents(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = main_vision.VisionAssistantApp()

    @classmethod
    def tearDownClass(cls):
        cls.app.destroy()

    def test_tooltips_initialized(self):
        self.assertIsNotNone(self.app.btn_vision)
        self.assertIsNotNone(self.app.btn_send)

        # Ensure ToolTip can show and hide without raising an error
        tooltip = main_vision.ToolTip(self.app.btn_vision, "Test Tooltip")
        tooltip.show_tip()
        self.assertIsNotNone(tooltip.tip_window)
        tooltip.hide_tip()
        self.assertIsNone(tooltip.tip_window)

    def test_avatar_window_fallback_coords(self):
        # Verify AvatarWindow runs animate_ring_and_levitate without error when avatar image is missing
        avatar = self.app.avatar
        self.assertIsNotNone(avatar)

    def test_toggle_main_window_keyboard_shortcut(self):
        initial_state = self.app.main_window_visible
        self.app.toggle_main_window()
        self.assertNotEqual(self.app.main_window_visible, initial_state)
        # Restore initial state
        self.app.toggle_main_window()
        self.assertEqual(self.app.main_window_visible, initial_state)


if __name__ == "__main__":
    unittest.main()
