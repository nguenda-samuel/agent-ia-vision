import unittest
from PIL import Image, ImageDraw
import numpy as np
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.filter = PrivacyFilter()

    def test_redact_sensitive_data_format_and_size(self):
        img = Image.new("RGB", (1000, 800), color=(255, 255, 255))
        redacted = self.filter.redact_sensitive_data(img)
        self.assertIsInstance(redacted, Image.Image)
        self.assertEqual(redacted.size, (1000, 800))
        self.assertEqual(redacted.mode, "RGB")

    def test_redact_sensitive_data_modifies_matching_field(self):
        # Create image with an input field (dark rectangle with white text/content inside)
        img = Image.new("RGB", (800, 600), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        draw.rectangle([100, 100, 300, 140], fill=(0, 0, 0))
        draw.text((110, 110), "SecretPassword123", fill=(255, 255, 255))

        redacted = self.filter.redact_sensitive_data(img)

        # The region inside the rectangle with text should be blurred/redacted
        orig_arr = np.array(img)
        redacted_arr = np.array(redacted)

        roi_orig = orig_arr[100:140, 100:300]
        roi_redacted = redacted_arr[100:140, 100:300]

        self.assertFalse(np.array_equal(roi_orig, roi_redacted))


if __name__ == "__main__":
    unittest.main()
