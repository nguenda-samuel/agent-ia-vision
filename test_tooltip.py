import os
import unittest
import tkinter as tk
import customtkinter as ctk

os.environ["SDL_AUDIODRIVER"] = "dummy"

from main_vision import CTkToolTip


class TestCTkToolTip(unittest.TestCase):

    def setUp(self):
        self.root = ctk.CTk()
        self.root.withdraw()
        self.button = ctk.CTkButton(self.root, text="🚀")
        self.button.pack()
        self.root.update()

    def tearDown(self):
        self.root.destroy()

    def test_tooltip_initialization(self):
        tooltip = CTkToolTip(self.button, "Envoyer la commande", delay_ms=100)
        self.assertEqual(tooltip.text, "Envoyer la commande")
        self.assertIsNone(tooltip.tooltip_window)
        self.assertIsNone(tooltip.timer_id)

    def test_tooltip_show_and_hide(self):
        tooltip = CTkToolTip(self.button, "Test Tooltip", delay_ms=50)

        # Test schedule_show
        tooltip.schedule_show()
        self.assertIsNotNone(tooltip.timer_id)

        # Trigger show directly
        tooltip.show()
        self.assertIsNotNone(tooltip.tooltip_window)
        self.assertTrue(tooltip.tooltip_window.winfo_exists())

        # Verify label content inside tooltip window
        children = tooltip.tooltip_window.winfo_children()
        self.assertEqual(len(children), 1)
        self.assertIsInstance(children[0], tk.Label)
        self.assertEqual(children[0].cget("text"), "Test Tooltip")

        # Test hide
        tooltip.hide()
        self.assertIsNone(tooltip.tooltip_window)
        self.assertIsNone(tooltip.timer_id)


if __name__ == "__main__":
    unittest.main()
