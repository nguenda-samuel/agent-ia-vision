import unittest
import numpy as np
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy_filter = PrivacyFilter()

    def test_redact_sensitive_data_shape_and_mode(self):
        # Create a sample RGB image (500x500)
        np_img = np.full((500, 500, 3), 250, dtype=np.uint8)
        np_img[100:140, 100:300] = 0  # dark rectangular region (w=200, h=40)
        pil_img = Image.fromarray(np_img, mode="RGB")

        redacted_img = self.privacy_filter.redact_sensitive_data(pil_img)

        self.assertIsInstance(redacted_img, Image.Image)
        self.assertEqual(redacted_img.size, (500, 500))
        self.assertEqual(redacted_img.mode, "RGB")

    def test_redact_sensitive_data_blurs_sensitive_rectangles(self):
        np_img = np.full((500, 500, 3), 250, dtype=np.uint8)
        # Create a rectangle with interior details matching contour criteria (100 < w < 400, 20 < h < 60)
        np_img[100:140, 100:300] = 0
        np_img[110:130, 120:280] = 200  # interior text/details
        pil_img = Image.fromarray(np_img, mode="RGB")

        redacted_img = self.privacy_filter.redact_sensitive_data(pil_img)
        redacted_np = np.array(redacted_img)

        # The interior region inside the rectangle should be blurred (smoothed out)
        self.assertFalse(np.array_equal(np_img[100:140, 100:300], redacted_np[100:140, 100:300]))


if __name__ == "__main__":
    unittest.main()
