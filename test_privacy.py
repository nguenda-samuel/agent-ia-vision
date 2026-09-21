import unittest
from PIL import Image
import numpy as np
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def test_redact_sensitive_data_resized(self):
        # Create a sample full HD image (1080, 1920, 3)
        img_np = np.random.randint(50, 200, (1080, 1920, 3), dtype=np.uint8)
        full_img = Image.fromarray(img_np)

        # Thumbnail the image to max 768x768 before redaction
        full_img.thumbnail((768, 768))
        self.assertLessEqual(full_img.width, 768)
        self.assertLessEqual(full_img.height, 768)

        privacy = PrivacyFilter()
        redacted_img = privacy.redact_sensitive_data(full_img)

        self.assertIsInstance(redacted_img, Image.Image)
        self.assertEqual(redacted_img.size, full_img.size)


if __name__ == "__main__":
    unittest.main()
