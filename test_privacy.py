import unittest
import numpy as np
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy = PrivacyFilter()

    def test_redact_sensitive_data_runs_without_error(self):
        # Image standard avec zone sombre simulant un champ de saisie (w=200, h=40)
        img_array = np.full((300, 500, 3), 200, dtype=np.uint8)
        img_array[50:90, 100:300] = 10  # zone sombre déclenchant findContours / boundingRect
        pil_img = Image.fromarray(img_array, mode="RGB")

        result = self.privacy.redact_sensitive_data(pil_img)
        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, (500, 300))

    def test_apply_blur_handles_small_rois(self):
        # ROI plus petite que le noyau de flou par défaut (ex: 20x20)
        small_roi = np.zeros((20, 20, 3), dtype=np.uint8)
        blurred = self.privacy._apply_blur(small_roi, max_kernel_size=51)
        self.assertIsNotNone(blurred)
        self.assertEqual(blurred.shape, (20, 20, 3))

    def test_apply_blur_handles_empty_roi(self):
        empty_roi = np.zeros((0, 0, 3), dtype=np.uint8)
        blurred = self.privacy._apply_blur(empty_roi, max_kernel_size=51)
        self.assertIsNone(blurred)


if __name__ == "__main__":
    unittest.main()
