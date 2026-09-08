import unittest
import numpy as np
from PIL import Image, ImageDraw
import cv2
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy_filter = PrivacyFilter()

    def test_redact_sensitive_data_dimensions_and_mode(self):
        # Create a sample RGB PIL image
        img = Image.new("RGB", (800, 600), color=(255, 255, 255))
        redacted = self.privacy_filter.redact_sensitive_data(img)

        self.assertIsInstance(redacted, Image.Image)
        self.assertEqual(redacted.size, (800, 600))
        self.assertEqual(redacted.mode, "RGB")

    def test_redact_sensitive_data_rectangular_inputs(self):
        # Create image with dark rectangle matching sensitive field dimensions
        img = Image.new("RGB", (800, 600), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        # Bounding box width = 200 (100 < w < 400), height = 30 (20 < h < 60)
        draw.rectangle([100, 100, 300, 130], fill=(0, 0, 0))

        redacted = self.privacy_filter.redact_sensitive_data(img)
        redacted_np = np.array(redacted)

        # Ensure the image was processed without error and returned as PIL image
        self.assertEqual(redacted_np.shape, (600, 800, 3))

    def test_redact_sensitive_data_pixel_equivalence(self):
        # Verify that operating in RGB directly produces identical results to RGB->BGR->RGB conversion
        img = Image.new("RGB", (500, 500), color=(200, 200, 200))
        draw = ImageDraw.Draw(img)
        draw.rectangle([50, 50, 250, 90], fill=(10, 10, 10))

        # Direct RGB processing (our optimized method)
        res_opt = self.privacy_filter.redact_sensitive_data(img)
        res_opt_np = np.array(res_opt)

        # Original RGB->BGR->RGB method
        open_cv_image = np.array(img)
        open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)

        faces = self.privacy_filter.face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
        )
        for x, y, w, h in faces:
            roi = open_cv_image[y : y + h, x : x + w]
            open_cv_image[y : y + h, x : x + w] = cv2.GaussianBlur(
                roi, (99, 99), 30
            )

        _, thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if 100 < w < 400 and 20 < h < 60:
                roi = open_cv_image[y : y + h, x : x + w]
                open_cv_image[y : y + h, x : x + w] = cv2.GaussianBlur(
                    roi, (51, 51), 0
                )

        res_orig_np = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2RGB)

        np.testing.assert_array_equal(res_opt_np, res_orig_np)


if __name__ == "__main__":
    unittest.main()
