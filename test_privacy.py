import unittest
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy_filter = PrivacyFilter()

    def test_redact_sensitive_data_rgb(self):
        img = Image.new("RGB", (200, 200), color=(255, 0, 0))
        result = self.privacy_filter.redact_sensitive_data(img)
        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.mode, "RGB")

    def test_redact_sensitive_data_rgba(self):
        img = Image.new("RGBA", (200, 200), color=(255, 0, 0, 255))
        result = self.privacy_filter.redact_sensitive_data(img)
        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.mode, "RGB")

    def test_redact_sensitive_data_grayscale(self):
        img = Image.new("L", (200, 200), color=128)
        result = self.privacy_filter.redact_sensitive_data(img)
        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.mode, "RGB")

    def test_redact_sensitive_data_palette(self):
        img = Image.new("P", (200, 200))
        result = self.privacy_filter.redact_sensitive_data(img)
        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.mode, "RGB")


if __name__ == "__main__":
    unittest.main()
