import unittest
import numpy as np
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy_filter = PrivacyFilter()

    def test_redact_sensitive_data_dimensions_and_mode(self):
        # Create a test image
        img_array = np.full((100, 100, 3), 200, dtype=np.uint8)
        pil_img = Image.fromarray(img_array, mode="RGB")

        result = self.privacy_filter.redact_sensitive_data(pil_img)

        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, (100, 100))
        self.assertEqual(result.mode, "RGB")

    def test_redact_sensitive_data_with_rectangles(self):
        # Create an image with a rectangular shape matching input field criteria (100 < w < 400 and 20 < h < 60)
        img_array = np.full((200, 500, 3), 200, dtype=np.uint8)
        # Draw dark rectangle outline and interior noise (simulating password input box)
        img_array[50:80, 50:200] = 10
        img_array[55:75, 60:190] = np.random.randint(0, 30, (20, 130, 3), dtype=np.uint8)
        pil_img = Image.fromarray(img_array, mode="RGB")

        result = self.privacy_filter.redact_sensitive_data(pil_img)

        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, (500, 200))
        result_array = np.array(result)
        # Verify that the image array was modified in the region (due to Gaussian blur)
        self.assertFalse(np.array_equal(result_array, img_array))


if __name__ == "__main__":
    unittest.main()
