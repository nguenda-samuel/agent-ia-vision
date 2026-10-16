import os
import sys
import unittest
from unittest.mock import MagicMock

os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["GEMINI_API_KEY"] = "dummy_test_key"

# Mock database module if not present
if "database" not in sys.modules:
    sys.modules["database"] = MagicMock()

import main_vision


class TestGUIUXImprovements(unittest.TestCase):

    def setUp(self):
        self.app = main_vision.VisionAssistantApp()

    def tearDown(self):
        try:
            self.app.destroy()
        except Exception:
            pass

    def test_app_initialization_and_hover_colors(self):
        """Vérifie que l'application s'initialise correctement et que les couleurs de survol sont configurées."""
        self.assertIsNotNone(self.app.btn_send)
        self.assertEqual(
            self.app.btn_send.cget("hover_color"),
            "#0773c5",
            "Le bouton d'envoi doit avoir une couleur de survol configurée pour le feedback visuel.",
        )
        self.assertEqual(
            self.app.quick_input.btn_send.cget("hover_color"),
            "#0773c5",
            "Le bouton d'envoi de la fenêtre rapide doit avoir une couleur de survol configurée.",
        )

    def test_buttons_disabled_during_processing(self):
        """Vérifie que les boutons d'action sont désactivés pendant le traitement async."""
        self.assertEqual(self.app.btn_send.cget("state"), "normal")
        self.assertEqual(self.app.btn_vision.cget("state"), "normal")

        # Déclenche process_request
        self.app.entry.insert(0, "Test prompt UX")
        self.app.process_request(use_vision=False)

        self.assertTrue(self.app.is_processing)
        self.assertEqual(
            self.app.btn_send.cget("state"),
            "disabled",
            "Le bouton d'envoi doit être désactivé pendant le traitement.",
        )
        self.assertEqual(
            self.app.btn_vision.cget("state"),
            "disabled",
            "Le bouton vision doit être désactivé pendant le traitement.",
        )


if __name__ == "__main__":
    unittest.main()
