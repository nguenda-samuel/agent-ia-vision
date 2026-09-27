import unittest
import customtkinter as ctk
from main_vision import CTkToolTip


class TestCTkToolTip(unittest.TestCase):

    def setUp(self):
        self.root = ctk.CTk()
        self.root.withdraw()
        self.button = ctk.CTkButton(self.root, text="📸")
        self.button.pack()
        self.tooltip = CTkToolTip(self.button, "Analyser l'écran (F9)")

    def tearDown(self):
        if self.tooltip.tooltip_window:
            self.tooltip.tooltip_window.destroy()
        self.root.destroy()

    def test_tooltip_creation_and_destruction(self):
        self.assertIsNone(self.tooltip.tooltip_window)

        # Simuler le survol / focus
        self.tooltip.show_tooltip()
        self.root.update()
        self.assertIsNotNone(self.tooltip.tooltip_window)

        # Simuler la sortie du curseur / perte de focus
        self.tooltip.hide_tooltip()
        self.root.update()
        self.assertIsNone(self.tooltip.tooltip_window)


if __name__ == "__main__":
    unittest.main()
