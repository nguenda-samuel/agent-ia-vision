import sys
from unittest.mock import MagicMock

sys.modules["database"] = MagicMock()

import tkinter as tk
import unittest

import customtkinter as ctk
from main_vision import CTkToolTip


class TestUIHelpers(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            cls.root = tk.Tk()
            cls.root.withdraw()
        except Exception:
            cls.root = None

    @classmethod
    def tearDownClass(cls):
        if cls.root:
            cls.root.destroy()

    def test_tooltip_creation(self):
        if not self.root:
            self.skipTest("No GUI display available")
        btn = ctk.CTkButton(self.root, text="🚀")
        tooltip = CTkToolTip(btn, "Test Tooltip")
        self.assertEqual(tooltip.text, "Test Tooltip")
        self.assertIsNone(tooltip.tooltip_window)


if __name__ == "__main__":
    unittest.main()
