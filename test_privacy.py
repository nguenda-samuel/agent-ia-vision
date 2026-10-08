import unittest
import numpy as np
from PIL import Image, ImageDraw
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy_filter = PrivacyFilter()

    def test_redact_sensitive_data_dimensions_and_type(self):
        img = Image.new("RGB", (600, 400), color=(200, 200, 200))
        result = self.privacy_filter.redact_sensitive_data(img)

        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, (600, 400))
        self.assertEqual(result.mode, "RGB")

    def test_redact_sensitive_data_with_rectangles(self):
        # Create an image with rectangular input-field like shapes
        img = Image.new("RGB", (800, 600), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        # Add a black box matching 100 < w < 400 and 20 < h < 60
        draw.rectangle([100, 100, 250, 140], fill=(0, 0, 0))

        result = self.privacy_filter.redact_sensitive_data(img)
        result_np = np.array(result)

        self.assertEqual(result.size, (800, 600))
        self.assertIsInstance(result_np, np.ndarray)


if __name__ == "__main__":
    unittest.main()
