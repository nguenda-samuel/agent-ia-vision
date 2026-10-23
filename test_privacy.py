import unittest
import numpy as np
from PIL import Image
import cv2
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy = PrivacyFilter()

    def test_redact_sensitive_data_dimensions_and_mode(self):
        # Create a dummy image
        width, height = 400, 300
        image = Image.new("RGB", (width, height), color=(200, 200, 200))

        redacted = self.privacy.redact_sensitive_data(image)

        self.assertEqual(redacted.size, (width, height))
        self.assertEqual(redacted.mode, "RGB")

    def test_redact_sensitive_data_applies_blur(self):
        # Create bright background with dark input box (w=151, h=31) containing colored content
        arr = np.full((300, 400, 3), 255, dtype=np.uint8)
        cv2.rectangle(arr, (100, 100), (250, 130), (0, 0, 0), -1)
        arr[110:120, 120:200] = [255, 0, 0] # Red bar inside box
        image = Image.fromarray(arr, mode="RGB")

        redacted = self.privacy.redact_sensitive_data(image)
        redacted_arr = np.array(redacted)

        # Check that the content inside the detected input box was blurred
        self.assertFalse(np.array_equal(arr, redacted_arr))


if __name__ == "__main__":
    unittest.main()
