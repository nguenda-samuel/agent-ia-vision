import unittest
import numpy as np
from PIL import Image
import cv2
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy_filter = PrivacyFilter()

    def test_redact_sensitive_data_output_format(self):
        # Create a test image (768x768 RGB)
        arr = np.random.randint(0, 256, (768, 768, 3), dtype=np.uint8)
        img = Image.fromarray(arr)

        redacted_img = self.privacy_filter.redact_sensitive_data(img)

        self.assertIsInstance(redacted_img, Image.Image)
        self.assertEqual(redacted_img.size, (768, 768))
        self.assertEqual(redacted_img.mode, "RGB")


if __name__ == "__main__":
    unittest.main()
