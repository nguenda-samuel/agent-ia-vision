import os
import sys
from unittest.mock import MagicMock

# Mock database module before main_vision is imported if not present
sys.modules["database"] = MagicMock()

import unittest
import tkinter as tk
import customtkinter as ctk

os.environ["GEMINI_API_KEY"] = "dummy_key"
os.environ["SDL_AUDIODRIVER"] = "dummy"

from main_vision import CTkToolTip


class TestCTkToolTip(unittest.TestCase):

    def setUp(self):
        self.root = ctk.CTk()
        self.btn = ctk.CTkButton(self.root, text="Test")
        self.btn.pack()

    def tearDown(self):
        self.root.destroy()

    def test_tooltip_creation_and_show(self):
        tooltip = CTkToolTip(self.btn, "Test tooltip text", delay=10)
        self.assertEqual(tooltip.text, "Test tooltip text")
        self.assertIsNone(tooltip.tooltip_window)

        tooltip.show()
        self.assertIsNotNone(tooltip.tooltip_window)
        self.assertTrue(tooltip.tooltip_window.winfo_exists())

        tooltip.hide()
        self.assertIsNone(tooltip.tooltip_window)


if __name__ == "__main__":
    unittest.main()
