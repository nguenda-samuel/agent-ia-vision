import sys
import unittest
from unittest.mock import MagicMock

# Mock database module if not present in environment
sys.modules["database"] = MagicMock()

import customtkinter as ctk
import main_vision


class TestToolTip(unittest.TestCase):

    def setUp(self):
        self.root = ctk.CTk()

    def tearDown(self):
        self.root.destroy()

    def test_tooltip_creation_and_hover(self):
        btn = ctk.CTkButton(self.root, text="🚀")
        btn.pack()
        self.root.update()

        tooltip = main_vision.ToolTip(btn, "Test ToolTip Text")
        self.assertIsNone(tooltip.tip_window)

        # Trigger hover enter
        tooltip.show_tip()
        self.root.update()
        self.assertIsNotNone(tooltip.tip_window)

        # Trigger hover leave
        tooltip.hide_tip()
        self.root.update()
        self.assertIsNone(tooltip.tip_window)


if __name__ == "__main__":
    unittest.main()
