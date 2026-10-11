import unittest
from PIL import Image, ImageDraw
import numpy as np
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy_filter = PrivacyFilter()

    def test_redact_sensitive_data_format_and_size(self):
        # Test with a synthetic RGB image containing potential rectangle regions
        img = Image.new("RGB", (1920, 1080), color=(240, 240, 240))
        draw = ImageDraw.Draw(img)
        # Draw some dark rectangular areas matching threshold criteria (100 < w < 400 and 20 < h < 60)
        for i in range(5):
            draw.rectangle(
                [100 + i * 50, 100 + i * 50, 250 + i * 50, 140 + i * 50],
                fill=(10, 10, 10),
            )

        redacted = self.privacy_filter.redact_sensitive_data(img)

        self.assertIsInstance(redacted, Image.Image)
        self.assertEqual(redacted.size, (1920, 1080))
        self.assertEqual(redacted.mode, "RGB")


if __name__ == "__main__":
    unittest.main()
