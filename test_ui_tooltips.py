import os
import sys
import unittest

# Mock database module if not present
sys.modules['database'] = type('db', (), {
    'get_cached_answer': lambda x: None,
    'save_answer': lambda x, y: None
})

import customtkinter as ctk
import main_vision
from main_vision import CTkToolTip, VisionAssistantApp


class TestUITooltips(unittest.TestCase):

    def setUp(self):
        os.environ["SDL_AUDIODRIVER"] = "dummy"
        os.environ["GEMINI_API_KEY"] = "dummy_key"
        self.root = ctk.CTk()
        self.root.withdraw()

    def tearDown(self):
        self.root.destroy()

    def test_tooltip_show_hide(self):
        btn = ctk.CTkButton(self.root, text="Test")
        tooltip = CTkToolTip(btn, "Hover Text")

        self.assertIsNone(tooltip.tip_window)

        tooltip.show()
        self.assertIsNotNone(tooltip.tip_window)

        tooltip.hide()
        self.assertIsNone(tooltip.tip_window)

    def test_app_buttons_and_tooltips(self):
        app = VisionAssistantApp()
        self.addCleanup(app.on_closing)

        self.assertEqual(app.btn_vision.cget("state"), "normal")
        self.assertEqual(app.btn_send.cget("state"), "normal")

        app.entry.insert(0, "Test instruction")
        app.process_request(use_vision=False)

        self.assertEqual(app.btn_vision.cget("state"), "disabled")
        self.assertEqual(app.btn_send.cget("state"), "disabled")


if __name__ == "__main__":
    unittest.main()
