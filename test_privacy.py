import unittest
from PIL import Image
import numpy as np
import cv2
from privacy import PrivacyFilter

class TestPrivacyFilter(unittest.TestCase):
    def setUp(self):
        self.filter = PrivacyFilter()

    def test_redact_sensitive_data_dimensions_and_type(self):
        img = Image.new("RGB", (800, 600), color=(128, 128, 128))
        redacted = self.filter.redact_sensitive_data(img)
        self.assertIsInstance(redacted, Image.Image)
        self.assertEqual(redacted.size, (800, 600))

    def test_redact_input_box(self):
        # Create an image with text inside a rectangular input box
        img_arr = np.full((600, 800, 3), 255, dtype=np.uint8)
        # Rectangle border
        cv2.rectangle(img_arr, (200, 200), (400, 230), (0, 0, 0), 2)
        # Some text inside
        cv2.putText(img_arr, "PASSWORD", (210, 222), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        img = Image.fromarray(img_arr)

        redacted = self.filter.redact_sensitive_data(img)
        redacted_arr = np.array(redacted)
        roi_orig = img_arr[200:230, 200:400]
        roi_redacted = redacted_arr[200:230, 200:400]
        self.assertFalse(np.array_equal(roi_orig, roi_redacted))

if __name__ == "__main__":
    unittest.main()
