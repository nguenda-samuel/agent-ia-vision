import unittest
import cv2
import numpy as np
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.pf = PrivacyFilter()

    def test_redact_no_sensitive_data_fast_path(self):
        """Verify fast-path returns original image when no faces or input boxes are present."""
        # Clean white image (no face, no dark threshold boxes)
        arr = np.full((300, 300, 3), 255, dtype=np.uint8)
        pil_img = Image.fromarray(arr)

        res = self.pf.redact_sensitive_data(pil_img)

        # Fast path returns exact same PIL Image object
        self.assertIs(res, pil_img)
        self.assertIsInstance(res, Image.Image)

    def test_redact_input_box(self):
        """Verify sensitive rectangular input fields are detected and redacted."""
        # Create image with a dark box matching 100 < w < 400 and 20 < h < 60
        # Inverse threshold will detect this as a contour
        arr = np.full((400, 400, 3), 255, dtype=np.uint8)
        # Draw dark rectangle (x=50, y=50, w=200, h=30)
        cv2.rectangle(arr, (50, 50), (250, 80), (0, 0, 0), -1)
        # Add white text/pattern inside the dark rectangle so blurring modifies pixel values
        cv2.putText(
            arr,
            "Secret",
            (60, 72),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2,
        )
        pil_img = Image.fromarray(arr)

        res = self.pf.redact_sensitive_data(pil_img)

        self.assertIsInstance(res, Image.Image)
        res_arr = np.array(res)

        # Before blurring, text pixels were pure white (255).
        # GaussianBlur on text inside dark box softens/blurs the text pixels.
        roi_orig = np.array(pil_img)[50:80, 50:250]
        roi_res = res_arr[50:80, 50:250]
        self.assertFalse(
            np.array_equal(roi_orig, roi_res), "ROI should be blurred and altered"
        )

    def test_redact_returns_correct_dimensions_and_mode(self):
        """Verify image dimensions and RGB mode are preserved."""
        arr = np.full((200, 300, 3), 128, dtype=np.uint8)
        pil_img = Image.fromarray(arr)

        res = self.pf.redact_sensitive_data(pil_img)

        self.assertEqual(res.size, (300, 200))
        self.assertEqual(res.mode, "RGB")


if __name__ == "__main__":
    unittest.main()
