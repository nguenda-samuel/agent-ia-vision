import unittest
import numpy as np
from PIL import Image
import cv2
from privacy import PrivacyFilter

class TestPrivacyFilter(unittest.TestCase):
    def setUp(self):
        self.pf = PrivacyFilter()

    def test_redact_sensitive_data_dimensions_and_type(self):
        img_arr = np.full((500, 500, 3), 200, dtype=np.uint8)
        cv2.rectangle(img_arr, (100, 100), (250, 130), (0, 0, 0), -1)
        pil_img = Image.fromarray(img_arr)

        res = self.pf.redact_sensitive_data(pil_img)
        self.assertIsInstance(res, Image.Image)
        self.assertEqual(res.size, pil_img.size)

    def test_redact_sensitive_data_input_field_blur(self):
        # Create a light image with a dark rectangle and text matching input field criteria
        img_arr = np.full((400, 400, 3), 200, dtype=np.uint8)
        cv2.rectangle(img_arr, (100, 100), (250, 130), (0, 0, 0), -1)
        cv2.putText(img_arr, "PASSWORD", (110, 122), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        pil_img = Image.fromarray(img_arr)

        res = self.pf.redact_sensitive_data(pil_img)
        res_arr = np.array(res)

        # Check that the text region inside the dark rectangle is blurred
        pixel_val = res_arr[120, 120]
        # Text was (255, 255, 255), after GaussianBlur with (0,0,0) background it becomes intermediate gray ~[77, 77, 77]
        self.assertFalse(np.array_equal(pixel_val, [255, 255, 255]))
        self.assertFalse(np.array_equal(pixel_val, [0, 0, 0]))

if __name__ == '__main__':
    unittest.main()
