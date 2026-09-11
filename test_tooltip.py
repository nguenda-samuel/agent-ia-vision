import os
import unittest
import customtkinter as ctk

# Ensure Pygame mixer uses dummy audio driver if imported
os.environ["SDL_AUDIODRIVER"] = "dummy"

from main_vision import CTkToolTip


class TestCTkToolTip(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.root = ctk.CTk()
        cls.root.withdraw()

    @classmethod
    def tearDownClass(cls):
        cls.root.destroy()

    def test_tooltip_creation_and_events(self):
        button = ctk.CTkButton(self.root, text="🚀")
        button.pack()
        self.root.update_idletasks()

        tooltip = CTkToolTip(button, "Envoyer la commande")
        self.assertIsNone(tooltip.tip_window)

        # Trigger hover enter event
        tooltip.show_tip()
        self.assertIsNotNone(tooltip.tip_window)
        self.assertTrue(tooltip.tip_window.winfo_exists())

        # Trigger hover leave event
        tooltip.hide_tip()
        self.assertIsNone(tooltip.tip_window)


if __name__ == "__main__":
    unittest.main()
