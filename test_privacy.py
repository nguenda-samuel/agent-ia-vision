import unittest
import numpy as np
import cv2
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy_filter = PrivacyFilter()

    def test_redact_sensitive_data_output_shape_and_type(self):
        # Create a test image of size 200x200
        np_img = np.zeros((200, 200, 3), dtype=np.uint8)
        pil_img = Image.fromarray(np_img)

        result = self.privacy_filter.redact_sensitive_data(pil_img)

        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, (200, 200))

    def test_redact_sensitive_data_with_faces_and_rectangles(self):
        # Create a synthetic image with a dark rectangle that triggers contour processing
        np_img = np.ones((768, 768, 3), dtype=np.uint8) * 200
        cv2.rectangle(np_img, (150, 150), (300, 190), (10, 10, 10), -1)
        pil_img = Image.fromarray(np_img)

        result = self.privacy_filter.redact_sensitive_data(pil_img)

        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, (768, 768))


if __name__ == "__main__":
    unittest.main()
