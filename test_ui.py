import os
import unittest
import customtkinter as ctk

# Set dummy env vars for headless environment
os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["GEMINI_API_KEY"] = "dummy_key"

from main_vision import CTkToolTip, VisionAssistantApp


class TestUIUX(unittest.TestCase):

    def setUp(self):
        self.root = ctk.CTk()
        self.root.withdraw()

    def tearDown(self):
        try:
            self.root.destroy()
        except Exception:
            pass

    def test_tooltip_creation_and_events(self):
        button = ctk.CTkButton(self.root, text="📸")
        tooltip = CTkToolTip(button, "Analyser l'écran (F9)")

        self.assertEqual(tooltip.text, "Analyser l'écran (F9)")
        self.assertIsNone(tooltip.tooltip_window)

        tooltip.show_tooltip()
        self.assertIsNotNone(tooltip.tooltip_window)

        tooltip.hide_tooltip()
        self.assertIsNone(tooltip.tooltip_window)

    def test_processing_state_disables_buttons(self):
        app = VisionAssistantApp()
        app.withdraw()

        # Initially processing should be False and buttons enabled ("normal")
        self.assertFalse(app.is_processing)
        self.assertEqual(app.btn_send.cget("state"), "normal")
        self.assertEqual(app.btn_vision.cget("state"), "disabled" if app.is_processing else "normal")

        # Set processing state to True
        app.set_processing_state(True)
        self.assertTrue(app.is_processing)
        self.assertEqual(app.btn_send.cget("state"), "disabled")
        self.assertEqual(app.btn_vision.cget("state"), "disabled")

        # Reset processing state to False
        app.set_processing_state(False)
        self.assertFalse(app.is_processing)
        self.assertEqual(app.btn_send.cget("state"), "normal")
        self.assertEqual(app.btn_vision.cget("state"), "normal")

        app.on_closing()


if __name__ == "__main__":
    unittest.main()
