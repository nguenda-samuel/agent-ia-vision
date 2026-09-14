import unittest
import numpy as np
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy_filter = PrivacyFilter()

    def test_redact_sensitive_data_dimensions_and_mode(self):
        """Verify redacted image has same dimensions and mode as input."""
        img_np = np.full((100, 100, 3), 200, dtype=np.uint8)
        pil_img = Image.fromarray(img_np, mode="RGB")

        redacted_img = self.privacy_filter.redact_sensitive_data(pil_img)

        self.assertEqual(redacted_img.size, pil_img.size)
        self.assertEqual(redacted_img.mode, "RGB")

    def test_redact_sensitive_data_rectangular_input_fields(self):
        """Verify dark box matching field threshold criteria is blurred."""
        # Create an image with a dark box matching (100 < w < 400 and 20 < h < 60)
        img_np = np.full((300, 300, 3), 200, dtype=np.uint8)
        # Draw dark box (width 150, height 30) with non-uniform content (e.g. text pattern)
        img_np[50:80, 50:200] = 10
        img_np[60:70, 60:190] = 255
        pil_img = Image.fromarray(img_np, mode="RGB")

        redacted_img = self.privacy_filter.redact_sensitive_data(pil_img)
        redacted_np = np.array(redacted_img)

        # Confirm the image is redacted (gaussian blurred box) and shape unchanged
        self.assertEqual(redacted_np.shape, img_np.shape)
        self.assertFalse(
            np.array_equal(
                redacted_np[50:80, 50:200], img_np[50:80, 50:200]
            )
        )


if __name__ == "__main__":
    unittest.main()
