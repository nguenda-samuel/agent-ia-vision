import unittest
import numpy as np
from PIL import Image, ImageDraw
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy_filter = PrivacyFilter()

    def test_redact_sensitive_data_output_format_and_size(self):
        """Test that redact_sensitive_data returns a PIL Image with identical dimensions."""
        img = Image.new("RGB", (800, 600), color=(240, 240, 240))
        result = self.privacy_filter.redact_sensitive_data(img)

        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, (800, 600))

    def test_redact_sensitive_data_with_rectangles(self):
        """Test that redact_sensitive_data processes rectangular input fields without error."""
        img = Image.new("RGB", (1280, 720), color=(240, 240, 240))
        draw = ImageDraw.Draw(img)
        # Draw rectangular fields matching condition (100 < w < 400 and 20 < h < 60)
        draw.rectangle([100, 100, 300, 140], fill=(10, 10, 10))
        draw.rectangle([100, 200, 250, 235], fill=(20, 20, 20))

        result = self.privacy_filter.redact_sensitive_data(img)
        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, (1280, 720))


if __name__ == "__main__":
    unittest.main()
