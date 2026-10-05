import os
import unittest

# Ensure headless environment settings
os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["GEMINI_API_KEY"] = "dummy_test_key"

import customtkinter as ctk
from main_vision import CTkToolTip, VisionAssistantApp


class TestCTkToolTip(unittest.TestCase):

    def setUp(self):
        self.app = ctk.CTk()

    def tearDown(self):
        self.app.destroy()

    def test_tooltip_creation_and_events(self):
        btn = ctk.CTkButton(self.app, text="🚀")
        tooltip = CTkToolTip(btn, "Test Tooltip")

        self.assertEqual(tooltip.text, "Test Tooltip")
        self.assertIsNone(tooltip.tooltip_window)

        tooltip.show_tooltip()
        self.assertIsNotNone(tooltip.tooltip_window)

        tooltip.hide_tooltip()
        self.assertIsNone(tooltip.tooltip_window)


class TestAppButtonStates(unittest.TestCase):

    def setUp(self):
        self.app = VisionAssistantApp()

    def tearDown(self):
        self.app.on_closing()

    def test_set_buttons_state(self):
        self.app.set_buttons_state("disabled")
        self.app.update()
        self.assertEqual(self.app.btn_vision.cget("state"), "disabled")
        self.assertEqual(self.app.btn_send.cget("state"), "disabled")

        self.app.set_buttons_state("normal")
        self.app.update()
        self.assertEqual(self.app.btn_vision.cget("state"), "normal")
        self.assertEqual(self.app.btn_send.cget("state"), "normal")


if __name__ == "__main__":
    unittest.main()
