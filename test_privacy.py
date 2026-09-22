import unittest
from PIL import Image, ImageDraw
import numpy as np
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.pf = PrivacyFilter()

    def test_redact_sensitive_data_dimensions_and_mode(self):
        # Create a sample RGB PIL image
        img = Image.new("RGB", (640, 480), color=(200, 200, 200))
        res = self.pf.redact_sensitive_data(img)

        self.assertIsInstance(res, Image.Image)
        self.assertEqual(res.size, (640, 480))
        self.assertEqual(res.mode, "RGB")

    def test_redact_sensitive_data_input_field_blur(self):
        # Create an image with a dark rectangular box with text matching contour size
        img = Image.new("RGB", (800, 600), color=(250, 250, 250))
        draw = ImageDraw.Draw(img)
        # Draw rectangular input box: w=200 (100 < w < 400), h=30 (20 < h < 60)
        draw.rectangle([100, 100, 300, 130], fill=(10, 10, 10))
        draw.text((110, 105), "SECRET_PASSWORD", fill=(200, 200, 200))

        res = self.pf.redact_sensitive_data(img)
        orig_arr = np.array(img)
        res_arr = np.array(res)

        # The region inside [100:130, 100:300] should be modified by GaussianBlur
        self.assertFalse(
            np.array_equal(
                orig_arr[100:130, 100:300], res_arr[100:130, 100:300]
            )
        )


if __name__ == "__main__":
    unittest.main()
