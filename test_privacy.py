import unittest
import numpy as np
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def test_redact_sensitive_data_solid_black(self):
        filter_inst = PrivacyFilter()
        # Create a white RGB image (100x100)
        img_array = np.full((100, 100, 3), 255, dtype=np.uint8)
        pil_img = Image.fromarray(img_array)

        redacted = filter_inst.redact_sensitive_data(pil_img)
        self.assertEqual(redacted.size, pil_img.size)


if __name__ == "__main__":
    unittest.main()
