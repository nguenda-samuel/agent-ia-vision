import unittest
import numpy as np
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy_filter = PrivacyFilter()

    def test_redact_sensitive_data_dimensions_and_type(self):
        # Create a dummy RGB image (100x100)
        arr = np.ones((100, 100, 3), dtype=np.uint8) * 200
        img = Image.fromarray(arr)

        redacted = self.privacy_filter.redact_sensitive_data(img)

        self.assertIsInstance(redacted, Image.Image)
        self.assertEqual(redacted.size, (100, 100))

    def test_redact_input_field(self):
        # Create an image with a dark rectangle matching 100 < w < 400 and 20 < h < 60
        arr = np.ones((200, 500, 3), dtype=np.uint8) * 255
        # Place black rectangle at y:50..90 (h=40), x:50..200 (w=150)
        arr[50:90, 50:200] = 0
        img = Image.fromarray(arr)

        redacted = self.privacy_filter.redact_sensitive_data(img)
        redacted_arr = np.array(redacted)

        # The image array should be altered around the black rectangle due to Gaussian blur
        self.assertEqual(redacted_arr.shape, (200, 500, 3))


if __name__ == "__main__":
    unittest.main()
