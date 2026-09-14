import os
import unittest
import tkinter as tk
import customtkinter as ctk

# Ensure headless execution works if run directly
from main_vision import CTkToolTip


class TestCTkToolTip(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            cls.root = ctk.CTk()
            cls.root.withdraw()
        except Exception as e:
            raise unittest.SkipTest(f"Display not available for GUI test: {e}")

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "root") and cls.root:
            cls.root.destroy()

    def test_tooltip_initialization_and_events(self):
        btn = ctk.CTkButton(self.root, text="🚀")
        tooltip = CTkToolTip(btn, "Test Tooltip", delay=50)

        self.assertEqual(tooltip.text, "Test Tooltip")
        self.assertIsNone(tooltip.tooltip_window)

        # Trigger schedule_tooltip
        tooltip.schedule_tooltip()
        self.assertIsNotNone(tooltip.id)

        # Force execution of scheduled after callbacks
        self.root.update()
        self.root.after(100)
        self.root.update()

        # Check tooltip window created
        self.assertIsNotNone(tooltip.tooltip_window)

        # Trigger hide_tooltip
        tooltip.hide_tooltip()
        self.assertIsNone(tooltip.tooltip_window)
        self.assertIsNone(tooltip.id)


if __name__ == "__main__":
    unittest.main()
