import unittest
import numpy as np
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy_filter = PrivacyFilter()

    def test_redact_sensitive_data_dimensions(self):
        """Test that redact_sensitive_data preserves image dimensions."""
        img = Image.fromarray(np.random.randint(0, 256, (1080, 1920, 3), dtype=np.uint8))
        result = self.privacy_filter.redact_sensitive_data(img)
        self.assertEqual(result.size, (1920, 1080))
        self.assertEqual(result.mode, "RGB")

    def test_redact_sensitive_data_small_image(self):
        """Test that redact_sensitive_data works properly on smaller images."""
        img = Image.fromarray(np.ones((100, 200, 3), dtype=np.uint8) * 128)
        result = self.privacy_filter.redact_sensitive_data(img)
        self.assertEqual(result.size, (200, 100))

    def test_redact_sensitive_data_rectangles(self):
        """Test redaction on synthetic rectangle matching contour thresholds."""
        img_arr = np.ones((500, 500, 3), dtype=np.uint8) * 200
        # Add dark rectangle (e.g. password box shape)
        img_arr[100:140, 100:300] = 10
        img = Image.fromarray(img_arr)
        result = self.privacy_filter.redact_sensitive_data(img)
        self.assertEqual(result.size, (500, 500))


if __name__ == "__main__":
    unittest.main()
