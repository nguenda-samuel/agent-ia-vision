import unittest
import numpy as np
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy_filter = PrivacyFilter()

    def test_redact_sensitive_data_returns_pil_image(self):
        # Create a sample 100x100 RGB image
        img_array = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
        img = Image.fromarray(img_array, mode="RGB")

        result = self.privacy_filter.redact_sensitive_data(img)

        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, (100, 100))
        self.assertEqual(result.mode, "RGB")

    def test_redact_sensitive_data_preserves_content_without_sensitive_elements(self):
        # Solid color image without faces or input fields
        img_array = np.full((200, 200, 3), 128, dtype=np.uint8)
        img = Image.fromarray(img_array, mode="RGB")

        result = self.privacy_filter.redact_sensitive_data(img)
        result_array = np.array(result)

        # Output should match input array
        np.testing.assert_array_equal(result_array, img_array)


if __name__ == "__main__":
    unittest.main()
