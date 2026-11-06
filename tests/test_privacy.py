import unittest
import numpy as np
from PIL import Image
import cv2
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy_filter = PrivacyFilter()

    def test_redact_sensitive_data_dimensions_and_mode(self):
        img = Image.new("RGB", (640, 480), color=(128, 128, 128))
        redacted = self.privacy_filter.redact_sensitive_data(img)

        self.assertEqual(redacted.size, (640, 480))
        self.assertEqual(redacted.mode, "RGB")

    def test_redact_sensitive_input_box(self):
        # Create an image with a dark box containing non-uniform contents (e.g. text dots)
        # matching the password/input field dimensions: width between 100 and 400, height between 20 and 60.
        arr = np.full((300, 500, 3), 255, dtype=np.uint8)
        # Draw dark rectangular box
        cv2.rectangle(arr, (100, 100), (300, 140), (10, 10, 10), -1)
        # Draw high-contrast text/dots inside the box so Gaussian blur alters pixel values
        cv2.putText(
            arr,
            "secret_pwd",
            (110, 125),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (25, 25, 25),
            1,
        )
        original_img = Image.fromarray(arr)

        redacted_img = self.privacy_filter.redact_sensitive_data(original_img)
        redacted_arr = np.array(redacted_img)

        # The bounding box area should be blurred (no longer identical to original)
        self.assertEqual(redacted_arr.shape, arr.shape)
        self.assertFalse(np.array_equal(arr, redacted_arr))

    def test_redact_sensitive_data_no_sensitive_content(self):
        # A uniform white image has no faces and no sensitive input boxes
        img = Image.new("RGB", (200, 200), color=(255, 255, 255))
        redacted = self.privacy_filter.redact_sensitive_data(img)
        self.assertTrue(np.array_equal(np.array(img), np.array(redacted)))


if __name__ == "__main__":
    unittest.main()
