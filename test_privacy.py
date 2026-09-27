import cv2
import numpy as np
from PIL import Image
import pytest

from privacy import PrivacyFilter


def test_redact_sensitive_data_dimensions_and_mode():
    privacy = PrivacyFilter()
    width, height = 800, 600
    img_array = np.full((height, width, 3), 128, dtype=np.uint8)
    pil_img = Image.fromarray(img_array)

    result_img = privacy.redact_sensitive_data(pil_img)

    assert isinstance(result_img, Image.Image)
    assert result_img.size == (width, height)
    assert result_img.mode == "RGB"


def test_redact_sensitive_data_input_field():
    privacy = PrivacyFilter()
    width, height = 1000, 800
    img_array = np.full((height, width, 3), 200, dtype=np.uint8)

    # Add a rectangular box matching sensitive input field dimensions (200x40 px)
    cv2.rectangle(img_array, (100, 100), (300, 140), (10, 10, 10), -1)
    pil_img = Image.fromarray(img_array)

    result_img = privacy.redact_sensitive_data(pil_img)
    result_array = np.array(result_img)

    assert result_array.shape == (height, width, 3)

    # Ensure Gaussian blurring modified pixels in the detected region
    diff = np.abs(img_array.astype(int) - result_array.astype(int))
    modified_pixel_count = np.sum(diff > 0)
    assert modified_pixel_count > 0


def test_redact_sensitive_data_various_sizes():
    privacy = PrivacyFilter()
    for size in [(320, 240), (1280, 720), (1920, 1080)]:
        width, height = size
        img_array = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
        pil_img = Image.fromarray(img_array)

        res = privacy.redact_sensitive_data(pil_img)
        assert res.size == (width, height)
