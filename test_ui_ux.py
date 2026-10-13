import os
import unittest
import tkinter as tk
import customtkinter as ctk

os.environ["GEMINI_API_KEY"] = "dummy_key_for_testing"
os.environ["SDL_AUDIODRIVER"] = "dummy"

from main_vision import CTkToolTip, VisionAssistantApp


class TestUIUXEnhancements(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = VisionAssistantApp()
        cls.app.update_idletasks()

    @classmethod
    def tearDownClass(cls):
        try:
            cls.app.on_closing()
        except Exception:
            pass

    def test_tooltip_creation_and_destruction(self):
        """Vérifie que CTkToolTip réagit aux événements Enter et Leave."""
        button = ctk.CTkButton(self.app, text="Test")
        button.pack()
        self.app.update()

        tooltip = CTkToolTip(button, "Test Tooltip")
        tooltip.show_tooltip()
        self.assertIsNotNone(tooltip.tooltip_window)

        tooltip.hide_tooltip()
        self.assertIsNone(tooltip.tooltip_window)

    def test_set_buttons_state(self):
        """Vérifie le basculement d'état (disabled / normal) des boutons."""
        self.app.set_buttons_state("disabled")
        self.assertEqual(self.app.btn_vision.cget("state"), "disabled")
        self.assertEqual(self.app.btn_send.cget("state"), "disabled")
        self.assertEqual(self.app.quick_input.btn_vision.cget("state"), "disabled")
        self.assertEqual(self.app.quick_input.btn_send.cget("state"), "disabled")

        self.app.set_buttons_state("normal")
        self.assertEqual(self.app.btn_vision.cget("state"), "normal")
        self.assertEqual(self.app.btn_send.cget("state"), "normal")
        self.assertEqual(self.app.quick_input.btn_vision.cget("state"), "normal")
        self.assertEqual(self.app.quick_input.btn_send.cget("state"), "normal")

    def test_stop_agent_workflow_resets_buttons(self):
        """Vérifie que stopper le workflow réactive les boutons."""
        self.app.set_buttons_state("disabled")
        self.app.stop_agent_workflow()
        self.assertEqual(self.app.btn_vision.cget("state"), "normal")
        self.assertEqual(self.app.btn_send.cget("state"), "normal")


if __name__ == "__main__":
    unittest.main()
