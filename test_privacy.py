import unittest
import numpy as np
import cv2
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.filter = PrivacyFilter()

    def test_redact_sensitive_data_output_size_and_type(self):
        # Create dummy RGB image (1920x1080)
        img_np = np.zeros((1080, 1920, 3), dtype=np.uint8) + 200
        # Draw a dark rectangle that simulates an input field with text
        cv2.rectangle(img_np, (500, 300), (700, 340), (10, 10, 10), -1)
        cv2.putText(
            img_np,
            "SECRET PASSWORD",
            (510, 325),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1,
        )

        pil_img = Image.fromarray(img_np)
        redacted = self.filter.redact_sensitive_data(pil_img)

        self.assertIsInstance(redacted, Image.Image)
        self.assertEqual(redacted.size, (1920, 1080))

        # Check that blurring occurred in the sensitive region
        redacted_np = np.array(redacted)
        self.assertFalse(
            np.array_equal(
                img_np[300:340, 500:700], redacted_np[300:340, 500:700]
            )
        )


if __name__ == "__main__":
    unittest.main()
