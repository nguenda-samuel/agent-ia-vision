import os
import sys
import unittest
from unittest.mock import MagicMock

# Mock database module before importing main_vision
sys.modules['database'] = MagicMock()
os.environ['GEMINI_API_KEY'] = 'dummy_key'

import customtkinter as ctk
import main_vision
from main_vision import CTkToolTip, VisionAssistantApp


class TestUIEnhancements(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ctk.set_appearance_mode("Dark")

    def setUp(self):
        self.root = ctk.CTk()

    def tearDown(self):
        self.root.destroy()

    def test_tooltip_show_and_hide(self):
        btn = ctk.CTkButton(self.root, text="Test")
        btn.pack()
        self.root.update()

        tooltip = CTkToolTip(btn, "Test tooltip text")
        self.assertIsNone(tooltip.tooltip_window)

        tooltip.show()
        self.root.update()
        self.assertIsNotNone(tooltip.tooltip_window)

        tooltip.hide()
        self.root.update()
        self.assertIsNone(tooltip.tooltip_window)

    def test_vision_assistant_app_buttons(self):
        app = VisionAssistantApp()
        self.root.update()

        # Check button texts
        self.assertIn("📸", app.btn_vision.cget("text"))
        self.assertIn("🚀", app.btn_send.cget("text"))

        app.destroy()


if __name__ == "__main__":
    unittest.main()
