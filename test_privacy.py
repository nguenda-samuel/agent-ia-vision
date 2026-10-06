import unittest
import numpy as np
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy = PrivacyFilter()

    def test_redact_sensitive_data_returns_pil_image(self):
        img_array = np.uint8(np.random.randint(0, 255, (200, 300, 3)))
        input_img = Image.fromarray(img_array)
        output_img = self.privacy.redact_sensitive_data(input_img)

        self.assertIsInstance(output_img, Image.Image)
        self.assertEqual(output_img.size, (300, 200))

    def test_redact_sensitive_data_dimensions(self):
        img_array = np.zeros((1080, 1920, 3), dtype=np.uint8)
        input_img = Image.fromarray(img_array)
        output_img = self.privacy.redact_sensitive_data(input_img)

        self.assertEqual(output_img.size, (1920, 1080))


if __name__ == "__main__":
    unittest.main()
