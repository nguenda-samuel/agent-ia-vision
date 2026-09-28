import os
import unittest
import tkinter as tk
import customtkinter as ctk

os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["GEMINI_API_KEY"] = "dummy_key"

from main_vision import ToolTip, VisionAssistantApp


class TestToolTipAndUX(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()

    def tearDown(self):
        try:
            self.root.destroy()
        except Exception:
            pass

    def test_tooltip_initialization_and_scheduling(self):
        btn = tk.Button(self.root, text="Test")
        btn.pack()
        tooltip = ToolTip(btn, "Test tooltip text")

        self.assertEqual(tooltip.text, "Test tooltip text")
        self.assertIsNone(tooltip.tip_window)
        self.assertIsNone(tooltip.id)

        # Test scheduling
        tooltip.schedule()
        self.assertIsNotNone(tooltip.id)

        # Test unschedule
        tooltip.unschedule()
        self.assertIsNone(tooltip.id)

    def test_tooltip_show_and_hide(self):
        btn = tk.Button(self.root, text="Test")
        btn.pack()
        tooltip = ToolTip(btn, "Test tooltip text")

        tooltip.showtip()
        self.assertIsNotNone(tooltip.tip_window)

        tooltip.hidetip()
        self.assertIsNone(tooltip.tip_window)

    def test_app_buttons_exist_and_have_tooltips(self):
        app = VisionAssistantApp()
        self.assertIsNotNone(app.btn_vision)
        self.assertIsNotNone(app.btn_send)
        self.assertEqual(app.btn_vision.cget("state"), "normal")
        self.assertEqual(app.btn_send.cget("state"), "normal")
        app.destroy()


if __name__ == "__main__":
    unittest.main()
