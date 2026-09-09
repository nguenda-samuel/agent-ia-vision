import os
import unittest
import tkinter as tk
import customtkinter as ctk

# Ensure Pygame uses dummy audio driver and GEMINI_API_KEY is present in test environment
os.environ["SDL_AUDIODRIVER"] = "dummy"
if "GEMINI_API_KEY" not in os.environ:
    os.environ["GEMINI_API_KEY"] = "test_key"

from main_vision import CTkToolTip, VisionAssistantApp, QuickInputWindow


class TestUXToolTips(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ctk.set_appearance_mode("Dark")

    def setUp(self):
        self.root = ctk.CTk()
        self.root.withdraw()

    def tearDown(self):
        self.root.destroy()

    def test_ctk_tooltip_show_and_hide(self):
        btn = ctk.CTkButton(self.root, text="🚀")
        btn.pack()
        self.root.update_idletasks()

        tooltip = CTkToolTip(btn, "Test Tooltip Text")
        self.assertIsNone(tooltip.tooltip_window)

        # Trigger show_tooltip
        tooltip.show_tooltip()
        self.assertIsNotNone(tooltip.tooltip_window)
        self.assertTrue(tooltip.tooltip_window.winfo_exists())

        # Check label text inside tooltip window
        children = tooltip.tooltip_window.winfo_children()
        self.assertEqual(len(children), 1)
        self.assertIsInstance(children[0], tk.Label)
        self.assertEqual(children[0].cget("text"), "Test Tooltip Text")

        # Trigger hide_tooltip
        tooltip.hide_tooltip()
        self.assertIsNone(tooltip.tooltip_window)

    def test_app_buttons_have_tooltips(self):
        # Instantiate VisionAssistantApp (without running mainloop)
        app = VisionAssistantApp()
        self.root.update_idletasks()

        try:
            # Check VisionAssistantApp icon buttons
            self.assertIsNotNone(app.btn_vision)
            self.assertIsNotNone(app.btn_send)

            # Check QuickInputWindow icon button
            self.assertIsNotNone(app.quick_input.btn_send)
        finally:
            app.destroy()


if __name__ == "__main__":
    unittest.main()
