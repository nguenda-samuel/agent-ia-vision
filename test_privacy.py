import unittest
import numpy as np
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy_filter = PrivacyFilter()

    def test_redact_sensitive_data_dimensions_and_mode(self):
        """Verify that output image maintains dimensions and RGB mode."""
        img_array = np.random.randint(0, 256, (200, 300, 3), dtype=np.uint8)
        pil_img = Image.fromarray(img_array, mode="RGB")

        result = self.privacy_filter.redact_sensitive_data(pil_img)

        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, (300, 200))
        self.assertEqual(result.mode, "RGB")

    def test_redact_sensitive_data_blank_image(self):
        """Verify processing on a blank (black) image."""
        img_array = np.zeros((100, 100, 3), dtype=np.uint8)
        pil_img = Image.fromarray(img_array, mode="RGB")

        result = self.privacy_filter.redact_sensitive_data(pil_img)

        self.assertEqual(result.size, (100, 100))


if __name__ == "__main__":
    unittest.main()
