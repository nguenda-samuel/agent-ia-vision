import unittest
import numpy as np
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy_filter = PrivacyFilter()

    def test_redact_sensitive_data_preserves_dimensions_and_mode(self):
        # Create a sample RGB image (200x200)
        img_array = np.random.randint(0, 256, (200, 200, 3), dtype=np.uint8)
        pil_img = Image.fromarray(img_array, mode="RGB")

        redacted_img = self.privacy_filter.redact_sensitive_data(pil_img)

        self.assertIsInstance(redacted_img, Image.Image)
        self.assertEqual(redacted_img.size, (200, 200))
        self.assertEqual(redacted_img.mode, "RGB")

    def test_redact_sensitive_data_color_integrity(self):
        # Create a solid color image (red: RGB 255, 0, 0) without faces or input fields
        img_array = np.zeros((100, 100, 3), dtype=np.uint8)
        img_array[:, :] = [255, 0, 0]
        pil_img = Image.fromarray(img_array, mode="RGB")

        redacted_img = self.privacy_filter.redact_sensitive_data(pil_img)
        res_array = np.array(redacted_img)

        # Ensure the output is still RGB red (channel 0 is 255, not swapped to BGR blue)
        self.assertEqual(res_array[0, 0, 0], 255)
        self.assertEqual(res_array[0, 0, 2], 0)


if __name__ == "__main__":
    unittest.main()
