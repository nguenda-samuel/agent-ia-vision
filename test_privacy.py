import unittest
import numpy as np
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy_filter = PrivacyFilter()

    def test_redact_sensitive_data_dimensions_and_type(self):
        # Create a synthetic 500x500 RGB image
        img_array = np.random.randint(0, 255, (500, 500, 3), dtype=np.uint8)
        input_image = Image.fromarray(img_array)

        output_image = self.privacy_filter.redact_sensitive_data(input_image)

        self.assertIsInstance(output_image, Image.Image)
        self.assertEqual(output_image.size, (500, 500))
        self.assertEqual(output_image.mode, "RGB")


if __name__ == "__main__":
    unittest.main()
