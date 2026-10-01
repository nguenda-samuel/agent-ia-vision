import unittest
import numpy as np
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy_filter = PrivacyFilter()

    def test_redact_sensitive_data_dimensions(self):
        # Test full 1080p image
        img_array = np.random.randint(0, 256, (1080, 1920, 3), dtype=np.uint8)
        pil_img = Image.fromarray(img_array, mode="RGB")

        result = self.privacy_filter.redact_sensitive_data(pil_img)

        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, (1920, 1080))
        self.assertEqual(result.mode, "RGB")

    def test_redact_sensitive_data_small_image(self):
        # Test smaller image (< 960px max dimension)
        img_array = np.random.randint(0, 256, (400, 600, 3), dtype=np.uint8)
        pil_img = Image.fromarray(img_array, mode="RGB")

        result = self.privacy_filter.redact_sensitive_data(pil_img)

        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, (600, 400))
        self.assertEqual(result.mode, "RGB")


if __name__ == "__main__":
    unittest.main()
