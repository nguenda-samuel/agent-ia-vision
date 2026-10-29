import unittest
from PIL import Image, ImageDraw
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy = PrivacyFilter()

    def test_redact_sensitive_data_dimensions(self):
        """Test that redact_sensitive_data preserves image dimensions."""
        img = Image.new("RGB", (1920, 1080), color="white")
        redacted_img = self.privacy.redact_sensitive_data(img)
        self.assertEqual(redacted_img.size, (1920, 1080))

    def test_redact_sensitive_data_rectangles(self):
        """Test redaction of input-field like rectangle."""
        img = Image.new("RGB", (800, 600), color="white")
        draw = ImageDraw.Draw(img)
        # Draw a black rectangle (simulating dark input field)
        draw.rectangle([200, 150, 400, 190], fill="black")
        redacted_img = self.privacy.redact_sensitive_data(img)
        self.assertEqual(redacted_img.size, (800, 600))


if __name__ == "__main__":
    unittest.main()
