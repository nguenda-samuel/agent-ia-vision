import unittest
from unittest.mock import MagicMock
import sys

# Mock missing optional/database dependency if database.py is absent
sys.modules['database'] = MagicMock()

import tkinter as tk
import customtkinter as ctk
from main_vision import ToolTip


class TestToolTip(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.root = ctk.CTk()
        cls.root.withdraw()

    @classmethod
    def tearDownClass(cls):
        cls.root.destroy()

    def test_tooltip_show_and_hide(self):
        button = ctk.CTkButton(self.root, text="🚀")
        tooltip = ToolTip(button, "Envoyer l'instruction")

        self.assertIsNone(tooltip.tip_window)

        tooltip.show_tip()
        self.assertIsNotNone(tooltip.tip_window)
        self.assertTrue(tooltip.tip_window.winfo_exists())

        tooltip.hide_tip()
        self.assertIsNone(tooltip.tip_window)

    def test_tooltip_empty_text(self):
        button = ctk.CTkButton(self.root, text="📸")
        tooltip = ToolTip(button, "")

        tooltip.show_tip()
        self.assertIsNone(tooltip.tip_window)


if __name__ == "__main__":
    unittest.main()
