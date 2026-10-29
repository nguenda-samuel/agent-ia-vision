import os
import sys
import unittest
from unittest.mock import MagicMock

# Mock database module before main_vision import if needed
sys.modules["database"] = MagicMock()
os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["GEMINI_API_KEY"] = "dummy_key"

import customtkinter as ctk
import main_vision
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
        btn = ctk.CTkButton(self.root, text="🚀")
        tooltip = ToolTip(btn, "Hover text test")

        self.assertIsNone(tooltip.tip_window)

        # Trigger show_tip
        tooltip.show_tip()
        self.root.update()
        self.assertIsNotNone(tooltip.tip_window)

        # Trigger hide_tip
        tooltip.hide_tip()
        self.root.update()
        self.assertIsNone(tooltip.tip_window)


if __name__ == "__main__":
    unittest.main()
