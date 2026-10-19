import unittest
import numpy as np
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.filter = PrivacyFilter()

    def test_redact_sensitive_data_return_type_and_size(self):
        # Create a test synthetic RGB image
        img_array = np.zeros((200, 300, 3), dtype=np.uint8)
        pil_img = Image.fromarray(img_array)

        redacted_img = self.filter.redact_sensitive_data(pil_img)

        self.assertIsInstance(redacted_img, Image.Image)
        self.assertEqual(redacted_img.size, (300, 200))
        self.assertEqual(redacted_img.mode, "RGB")

    def test_redact_sensitive_data_rectangles(self):
        # Create image with a rectangle matching sensitive field dimensions (e.g. 200x30)
        img_array = np.full((300, 400, 3), 255, dtype=np.uint8)
        # Draw a dark box (100 < w < 400 and 20 < h < 60)
        img_array[50:90, 50:250] = 0
        pil_img = Image.fromarray(img_array)

        redacted_img = self.filter.redact_sensitive_data(pil_img)
        self.assertIsInstance(redacted_img, Image.Image)
        self.assertEqual(redacted_img.size, (400, 300))


if __name__ == "__main__":
    unittest.main()
