import unittest
import numpy as np
from PIL import Image, ImageDraw
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy_filter = PrivacyFilter()

    def test_redact_sensitive_data_return_type_and_dimensions(self):
        img = Image.new("RGB", (800, 600), color=(255, 255, 255))
        result = self.privacy_filter.redact_sensitive_data(img)
        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, (800, 600))
        self.assertEqual(result.mode, "RGB")

    def test_redact_sensitive_data_obfuscates_input_fields(self):
        img = Image.new("RGB", (800, 600), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        # Draw a dark input box with text inside (w=151, h=31)
        draw.rectangle([200, 200, 350, 230], fill=(0, 0, 0))
        draw.text((210, 210), "SecretPassword", fill=(255, 255, 255))

        original_arr = np.array(img)
        result = self.privacy_filter.redact_sensitive_data(img)
        result_arr = np.array(result)

        # Check that the rectangle area was modified/redacted
        rect_roi_orig = original_arr[200:230, 200:350]
        rect_roi_res = result_arr[200:230, 200:350]
        self.assertFalse(np.array_equal(rect_roi_orig, rect_roi_res))


if __name__ == "__main__":
    unittest.main()
