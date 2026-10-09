import sys
import unittest
from unittest.mock import MagicMock

# Mock database module which is not present in repo before importing main_vision
sys.modules["database"] = MagicMock()

import tkinter as tk
import customtkinter as ctk

from main_vision import Tooltip


class TestTooltip(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.button = tk.Button(self.root, text="🚀")
        self.button.pack()
        self.root.update_idletasks()

    def tearDown(self):
        self.root.destroy()

    def test_tooltip_creation_and_events(self):
        tooltip = Tooltip(self.button, "Test Tooltip")
        self.assertIsNone(tooltip.tooltip_window)

        tooltip.show_tooltip()
        self.assertIsNotNone(tooltip.tooltip_window)
        self.assertTrue(tooltip.tooltip_window.winfo_exists())

        tooltip.hide_tooltip()
        self.assertIsNone(tooltip.tooltip_window)

    def test_tooltip_empty_text(self):
        tooltip = Tooltip(self.button, "")
        tooltip.show_tooltip()
        self.assertIsNone(tooltip.tooltip_window)


if __name__ == "__main__":
    unittest.main()
