import unittest
import numpy as np
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.pf = PrivacyFilter()

    def test_redact_sensitive_data_dimensions_and_type(self):
        # Create a test image
        img_arr = np.zeros((400, 600, 3), dtype=np.uint8)
        pil_img = Image.fromarray(img_arr)

        redacted = self.pf.redact_sensitive_data(pil_img)

        self.assertIsInstance(redacted, Image.Image)
        self.assertEqual(redacted.size, (600, 400))


if __name__ == "__main__":
    unittest.main()
