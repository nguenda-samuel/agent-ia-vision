import unittest
import numpy as np
from PIL import Image
import cv2
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy = PrivacyFilter()

    def test_redact_sensitive_data_dimensions_and_type(self):
        # Create a simple test PIL Image
        arr = np.full((100, 100, 3), 200, dtype=np.uint8)
        img = Image.fromarray(arr)

        redacted = self.privacy.redact_sensitive_data(img)

        self.assertIsInstance(redacted, Image.Image)
        self.assertEqual(redacted.size, (100, 100))
        self.assertEqual(redacted.mode, "RGB")

    def test_redact_sensitive_data_rectangular_fields(self):
        # Create image with dark rectangle matching 100<w<400 and 20<h<60
        arr = np.full((300, 500, 3), 240, dtype=np.uint8)
        # Draw dark rectangle (simulate password input box)
        cv2.rectangle(arr, (50, 50), (250, 90), (10, 10, 10), -1)
        img = Image.fromarray(arr)

        redacted = self.privacy.redact_sensitive_data(img)
        redacted_np = np.array(redacted)

        # Confirm the output is an RGB image with same shape
        self.assertEqual(redacted_np.shape, (300, 500, 3))


if __name__ == "__main__":
    unittest.main()
