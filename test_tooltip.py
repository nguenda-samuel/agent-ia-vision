import unittest
import tkinter as tk
from main_vision import ToolTip

class TestToolTip(unittest.TestCase):
    def setUp(self):
        try:
            self.root = tk.Tk()
            self.root.withdraw()
        except Exception as e:
            self.skipTest(f"Tkinter root cannot be initialized: {e}")

    def tearDown(self):
        if hasattr(self, 'root') and self.root:
            self.root.destroy()

    def test_tooltip_creation_and_destruction(self):
        button = tk.Button(self.root, text="Test")
        button.pack()
        self.root.update_idletasks()

        tooltip = ToolTip(button, "Test Tooltip Text")
        self.assertIsNone(tooltip.tooltip_window)

        # Simulate show_tooltip
        tooltip.show_tooltip()
        self.assertIsNotNone(tooltip.tooltip_window)
        self.assertTrue(tooltip.tooltip_window.winfo_exists())

        # Simulate hide_tooltip
        tooltip.hide_tooltip()
        self.assertIsNone(tooltip.tooltip_window)

if __name__ == "__main__":
    unittest.main()
