import unittest
import numpy as np
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy_filter = PrivacyFilter()

    def test_redact_sensitive_data_dimensions_and_mode(self):
        # Create a sample image (RGB, 800x600)
        img_array = np.full((600, 800, 3), 200, dtype=np.uint8)
        input_img = Image.fromarray(img_array, mode="RGB")

        result_img = self.privacy_filter.redact_sensitive_data(input_img)

        self.assertIsInstance(result_img, Image.Image)
        self.assertEqual(result_img.size, (800, 600))
        self.assertEqual(result_img.mode, "RGB")

    def test_redact_sensitive_data_with_dark_rectangle(self):
        # Create image with dark rectangle matching sensitive field contour dimensions (w ~ 200, h ~ 40)
        img_array = np.full((600, 800, 3), 255, dtype=np.uint8)
        # Draw dark box on white background
        img_array[100:140, 100:300] = 0
        input_img = Image.fromarray(img_array, mode="RGB")

        result_img = self.privacy_filter.redact_sensitive_data(input_img)

        self.assertIsInstance(result_img, Image.Image)
        self.assertEqual(result_img.size, (800, 600))


if __name__ == "__main__":
    unittest.main()
