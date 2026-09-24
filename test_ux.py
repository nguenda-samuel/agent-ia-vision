import os
import unittest

import customtkinter as ctk

os.environ["GEMINI_API_KEY"] = "dummy_key"
os.environ["SDL_AUDIODRIVER"] = "dummy"

from main_vision import CTkToolTip, VisionAssistantApp


class TestToolTipUX(unittest.TestCase):

    def setUp(self):
        self.app = VisionAssistantApp()

    def tearDown(self):
        try:
            self.app.destroy()
        except Exception:
            pass

    def test_tooltip_initialization(self):
        button = ctk.CTkButton(self.app, text="Test")
        tooltip = CTkToolTip(button, "Test Tooltip")
        self.assertEqual(tooltip.text, "Test Tooltip")
        tooltip.schedule_show()
        self.assertIsNotNone(tooltip.timer_id)
        tooltip.hide_tooltip()
        self.assertIsNone(tooltip.timer_id)


if __name__ == "__main__":
    unittest.main()
