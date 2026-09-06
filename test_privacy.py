import unittest
import numpy as np
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy_filter = PrivacyFilter()

    def test_redact_sensitive_data_dimensions_and_mode(self):
        # Create dummy image
        img_array = np.full((200, 300, 3), 128, dtype=np.uint8)
        img = Image.fromarray(img_array, mode="RGB")

        result = self.privacy_filter.redact_sensitive_data(img)

        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, (300, 200))
        self.assertEqual(result.mode, "RGB")

    def test_redact_sensitive_data_no_faces_or_inputs(self):
        # Image with uniform color (no faces or rectangular input fields)
        img_array = np.full((100, 100, 3), 200, dtype=np.uint8)
        img = Image.fromarray(img_array, mode="RGB")

        result = self.privacy_filter.redact_sensitive_data(img)
        res_array = np.array(result)

        # Image should be unchanged
        np.testing.assert_array_equal(res_array, img_array)


if __name__ == "__main__":
    unittest.main()
