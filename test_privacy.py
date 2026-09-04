import unittest
import numpy as np
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy_filter = PrivacyFilter()

    def test_redact_sensitive_data_output_format(self):
        # Create a dummy image (RGB 100x100)
        np_img = np.zeros((100, 100, 3), dtype=np.uint8)
        img = Image.fromarray(np_img)

        result = self.privacy_filter.redact_sensitive_data(img)

        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, (100, 100))

    def test_redact_sensitive_data_different_dimensions(self):
        # Create a dummy image with typical screen resolution (1920x1080)
        np_img = np.random.randint(0, 256, (1080, 1920, 3), dtype=np.uint8)
        img = Image.fromarray(np_img)

        result = self.privacy_filter.redact_sensitive_data(img)

        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, (1920, 1080))


if __name__ == "__main__":
    unittest.main()
