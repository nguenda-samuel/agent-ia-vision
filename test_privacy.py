import unittest
import numpy as np
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.filter = PrivacyFilter()

    def test_redact_sensitive_data_output_format(self):
        # Create a blank RGB test image
        img_array = np.full((100, 100, 3), 200, dtype=np.uint8)
        img = Image.fromarray(img_array)

        redacted = self.filter.redact_sensitive_data(img)
        self.assertIsInstance(redacted, Image.Image)
        self.assertEqual(redacted.size, (100, 100))
        self.assertEqual(redacted.mode, "RGB")

    def test_redact_sensitive_data_rectangles(self):
        # Create an image with a dark rectangle matching sensitive field dimensions
        img_array = np.full((300, 500, 3), 200, dtype=np.uint8)
        # Draw a dark input rectangle (w=200, h=40)
        img_array[100:140, 100:300] = 10
        img = Image.fromarray(img_array)

        redacted = self.filter.redact_sensitive_data(img)
        redacted_array = np.array(redacted)

        # Confirm image dimensions are unchanged and data is array-like
        self.assertEqual(redacted_array.shape, (300, 500, 3))


if __name__ == "__main__":
    unittest.main()
