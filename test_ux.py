import os
import unittest

# Ensure headless execution for tests
os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["GEMINI_API_KEY"] = "mock_api_key_for_testing"

from main_vision import CTkToolTip, VisionAssistantApp


class TestUXEnhancements(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            cls.app = VisionAssistantApp()
            cls.app.update_idletasks()
        except Exception as e:
            raise unittest.SkipTest(f"GUI not available: {e}")

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "app"):
            try:
                cls.app.destroy()
            except Exception:
                pass

    def test_tooltip_creation_and_events(self):
        btn = self.app.btn_vision
        tooltip = CTkToolTip(btn, "Analyser l'écran (📸)")
        self.assertEqual(tooltip.text, "Analyser l'écran (📸)")

        tooltip.show_tooltip()
        self.assertIsNotNone(tooltip.tooltip_window)

        tooltip.hide_tooltip()
        self.assertIsNone(tooltip.tooltip_window)

    def test_processing_state_toggles_buttons(self):
        # Set processing state to True -> buttons should be disabled
        self.app.set_processing_state(True)
        self.assertTrue(self.app.is_processing)
        self.assertEqual(self.app.btn_send.cget("state"), "disabled")
        self.assertEqual(self.app.btn_vision.cget("state"), "disabled")

        # Set processing state to False -> buttons should be enabled
        self.app.set_processing_state(False)
        self.assertFalse(self.app.is_processing)
        self.assertEqual(self.app.btn_send.cget("state"), "normal")
        self.assertEqual(self.app.btn_vision.cget("state"), "normal")


if __name__ == "__main__":
    unittest.main()
