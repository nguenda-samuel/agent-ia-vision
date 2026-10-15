import os
import unittest

os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["GEMINI_API_KEY"] = "dummy_key"

import customtkinter as ctk
from main_vision import CTkToolTip, VisionAssistantApp


class TestUXEnhancements(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ctk.set_appearance_mode("Dark")

    def setUp(self):
        self.root = ctk.CTk()
        self.root.withdraw()

    def tearDown(self):
        self.root.destroy()

    def test_tooltip_show_and_hide(self):
        btn = ctk.CTkButton(self.root, text="🚀")
        btn.pack()
        self.root.update_idletasks()

        tooltip = CTkToolTip(btn, "Test Tooltip")
        self.assertIsNone(tooltip.tooltip_window)

        tooltip.show()
        self.root.update_idletasks()
        self.assertIsNotNone(tooltip.tooltip_window)

        tooltip.hide()
        self.root.update_idletasks()
        self.assertIsNone(tooltip.tooltip_window)

    def test_app_toggle_main_window_focus(self):
        app = VisionAssistantApp()
        self.assertFalse(app.main_window_visible)

        app.toggle_main_window()
        app.update()

        self.assertTrue(app.main_window_visible)
        self.assertIn(app.focus_get(), (app.entry, app.entry._entry, app))

        app.on_closing()

    def test_app_escape_key_hides_window(self):
        app = VisionAssistantApp()
        app.toggle_main_window()
        app.update_idletasks()
        self.assertTrue(app.main_window_visible)

        app.event_generate("<Escape>")
        app.update_idletasks()
        self.assertFalse(app.main_window_visible)

        app.on_closing()


if __name__ == "__main__":
    unittest.main()
