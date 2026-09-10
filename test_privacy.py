import unittest
import numpy as np
import cv2
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy_filter = PrivacyFilter()

    def test_redact_sensitive_data_dimensions_and_type(self):
        # Create a test PIL image (1000x600)
        img_arr = np.zeros((600, 1000, 3), dtype=np.uint8) + 200
        # Draw a dark box resembling a password input field
        cv2.rectangle(img_arr, (100, 100), (300, 130), (10, 10, 10), -1)
        test_img = Image.fromarray(img_arr)

        redacted_img = self.privacy_filter.redact_sensitive_data(test_img)

        self.assertIsInstance(redacted_img, Image.Image)
        self.assertEqual(redacted_img.size, test_img.size)

    def test_redact_sensitive_data_empty_image(self):
        test_img = Image.new("RGB", (100, 100), color="white")
        redacted_img = self.privacy_filter.redact_sensitive_data(test_img)
        self.assertIsInstance(redacted_img, Image.Image)
        self.assertEqual(redacted_img.size, (100, 100))


if __name__ == "__main__":
    unittest.main()
