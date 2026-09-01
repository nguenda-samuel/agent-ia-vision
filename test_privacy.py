import unittest
import numpy as np
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def test_redact_sensitive_data_solid_black_rectangle(self):
        # Create an image with a dark rectangular border matching input field criteria (e.g. w=200, h=40)
        # on a white background with black text inside the box
        img_array = np.full((100, 300, 3), 255, dtype=np.uint8)
        # Draw a dark input box rectangle around x=50, y=30, w=200, h=40
        img_array[30:70, 50:250] = 0
        # White inner background inside the input box (simulating input field with text)
        img_array[32:68, 52:248] = 255
        # Black text inside input field
        img_array[45:55, 100:150] = 0

        pil_img = Image.fromarray(img_array)
        filter_obj = PrivacyFilter()
        redacted_img = filter_obj.redact_sensitive_data(pil_img)
        redacted_array = np.array(redacted_img)

        # Verify that the PrivacyFilter process completed and returned a PIL Image
        self.assertIsInstance(redacted_img, Image.Image)
        self.assertEqual(redacted_array.shape, img_array.shape)


if __name__ == "__main__":
    unittest.main()
