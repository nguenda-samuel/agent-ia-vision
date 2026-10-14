import unittest
import numpy as np
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy_filter = PrivacyFilter()

    def test_redact_sensitive_data_dimensions_and_type(self):
        # Create dummy RGB PIL image (800x600)
        img_array = np.random.randint(0, 256, (600, 800, 3), dtype=np.uint8)
        input_img = Image.fromarray(img_array)

        result_img = self.privacy_filter.redact_sensitive_data(input_img)

        self.assertIsInstance(result_img, Image.Image)
        self.assertEqual(result_img.size, (800, 600))
        self.assertEqual(result_img.mode, "RGB")

    def test_redact_sensitive_data_small_image(self):
        # Test with a smaller image (200x200)
        img_array = np.zeros((200, 200, 3), dtype=np.uint8)
        input_img = Image.fromarray(img_array)

        result_img = self.privacy_filter.redact_sensitive_data(input_img)

        self.assertIsInstance(result_img, Image.Image)
        self.assertEqual(result_img.size, (200, 200))


if __name__ == "__main__":
    unittest.main()
