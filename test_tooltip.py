import os
import unittest
import tkinter as tk
import customtkinter as ctk

os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["GEMINI_API_KEY"] = "dummy_key"

from main_vision import CTkToolTip, VisionAssistantApp


class TestCTkToolTip(unittest.TestCase):

    def setUp(self):
        self.root = ctk.CTk()
        self.root.withdraw()
        self.button = ctk.CTkButton(self.root, text="📸")
        self.button.pack()
        self.root.update_idletasks()

    def tearDown(self):
        self.root.destroy()

    def test_tooltip_show_and_hide(self):
        tooltip = CTkToolTip(self.button, "Test Tooltip Description")
        self.assertIsNone(tooltip.tip_window)

        # Simulate hover event
        tooltip.show_tip()
        self.root.update_idletasks()
        self.assertIsNotNone(tooltip.tip_window)

        # Simulate leave event
        tooltip.hide_tip()
        self.root.update_idletasks()
        self.assertIsNone(tooltip.tip_window)


class TestVisionAssistantAppProcessingUI(unittest.TestCase):

    def setUp(self):
        self.app = VisionAssistantApp()
        self.app.withdraw()
        self.app.update_idletasks()

    def tearDown(self):
        self.app.on_closing()

    def test_set_processing_ui_disabled_and_enabled(self):
        # Enable processing mode
        self.app.set_processing_ui(True)
        self.app.update_idletasks()

        self.assertEqual(self.app.btn_vision.cget("state"), "disabled")
        self.assertEqual(self.app.btn_send.cget("state"), "disabled")
        self.assertEqual(self.app.btn_send.cget("text"), "⏳")
        self.assertEqual(self.app.quick_input.btn_vision.cget("state"), "disabled")
        self.assertEqual(self.app.quick_input.btn_send.cget("state"), "disabled")
        self.assertEqual(self.app.quick_input.btn_send.cget("text"), "⏳")

        # Disable processing mode
        self.app.set_processing_ui(False)
        self.app.update_idletasks()

        self.assertEqual(self.app.btn_vision.cget("state"), "normal")
        self.assertEqual(self.app.btn_send.cget("state"), "normal")
        self.assertEqual(self.app.btn_send.cget("text"), "🚀")
        self.assertEqual(self.app.quick_input.btn_vision.cget("state"), "normal")
        self.assertEqual(self.app.quick_input.btn_send.cget("state"), "normal")
        self.assertEqual(self.app.quick_input.btn_send.cget("text"), "🚀")


if __name__ == "__main__":
    unittest.main()
