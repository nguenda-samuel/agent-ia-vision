import os
import sys
import unittest
from unittest.mock import MagicMock

os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["GEMINI_API_KEY"] = "dummy_test_key"

# Mock database module if not present in test environment
if "database" not in sys.modules:
    sys.modules["database"] = MagicMock()

import customtkinter as ctk
import main_vision


class TestCTkToolTip(unittest.TestCase):

    def setUp(self):
        self.root = ctk.CTk()

    def tearDown(self):
        try:
            self.root.destroy()
        except Exception:
            pass

    def test_tooltip_show_and_hide(self):
        """Vérifie que CTkToolTip s'affiche et se masque correctement."""
        btn = ctk.CTkButton(self.root, text="🚀")
        btn.pack(padx=20, pady=20)
        self.root.update()

        tooltip = main_vision.CTkToolTip(btn, "Action test", delay=10)
        self.assertIsNone(tooltip.tip_window)

        # Affiche l'infobulle
        tooltip.show_tip()
        self.root.update()
        self.assertIsNotNone(
            tooltip.tip_window, "La fenêtre de l'infobulle devrait être créée"
        )
        self.assertTrue(tooltip.tip_window.winfo_exists())

        # Masque l'infobulle
        tooltip.hide_tip()
        self.root.update()
        self.assertIsNone(
            tooltip.tip_window,
            "La fenêtre de l'infobulle devrait être détruite",
        )

    def test_vision_assistant_app_initialization(self):
        """Vérifie que VisionAssistantApp s'initialise avec les boutons et l'avatar sans erreur."""
        app = main_vision.VisionAssistantApp()
        try:
            app.update()
            self.assertIsNotNone(app.btn_vision)
            self.assertIsNotNone(app.btn_send)
            self.assertIsNotNone(app.quick_input.btn_send)
            self.assertIsNotNone(app.avatar)
        finally:
            app.destroy()


if __name__ == "__main__":
    unittest.main()
