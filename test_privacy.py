import unittest
import numpy as np
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy_filter = PrivacyFilter()

    def test_redact_sensitive_data_return_type_and_size(self):
        """Test that redact_sensitive_data returns a PIL Image with matching dimensions."""
        width, height = 400, 300
        img_array = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
        pil_image = Image.fromarray(img_array)

        redacted_image = self.privacy_filter.redact_sensitive_data(pil_image)

        self.assertIsInstance(redacted_image, Image.Image)
        self.assertEqual(redacted_image.size, (width, height))

    def test_redact_sensitive_data_small_image(self):
        """Test redact_sensitive_data with small image dimensions."""
        width, height = 50, 50
        img_array = np.zeros((height, width, 3), dtype=np.uint8)
        pil_image = Image.fromarray(img_array)

        redacted_image = self.privacy_filter.redact_sensitive_data(pil_image)

        self.assertIsInstance(redacted_image, Image.Image)
        self.assertEqual(redacted_image.size, (width, height))

    def test_redact_sensitive_data_input_field_box(self):
        """Test redact_sensitive_data handles images with rectangular input box regions."""
        width, height = 500, 500
        img_array = np.full((height, width, 3), 255, dtype=np.uint8)
        # Create a dark rectangular box matching input field contours
        img_array[100:140, 100:300] = 0
        pil_image = Image.fromarray(img_array)

        redacted_image = self.privacy_filter.redact_sensitive_data(pil_image)

        self.assertIsInstance(redacted_image, Image.Image)
        self.assertEqual(redacted_image.size, (width, height))


if __name__ == "__main__":
    unittest.main()
