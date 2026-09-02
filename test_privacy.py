import numpy as np
from PIL import Image, ImageDraw
from privacy import PrivacyFilter


def test_privacy_filter_redact_sensitive_data():
    filter_obj = PrivacyFilter()

    # Create a test image with a mock input box containing text/pattern
    img = Image.new("RGB", (800, 600), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    # Draw a rectangular input field outline and text inside
    # Rectangle coordinates: x0=100, y0=100, x1=300 (w=200), y1=130 (h=30)
    draw.rectangle([100, 100, 300, 130], fill=(255, 255, 255), outline=(0, 0, 0))
    # Draw pattern/text inside box
    draw.line([120, 115, 280, 115], fill=(0, 0, 0), width=3)

    result = filter_obj.redact_sensitive_data(img)

    assert isinstance(result, Image.Image)
    assert result.size == (800, 600)
    assert result.mode == "RGB"

    # Verify that the image in the ROI region has been modified (blurred)
    orig_roi = np.array(img)[100:130, 100:300]
    res_roi = np.array(result)[100:130, 100:300]
    assert not np.array_equal(orig_roi, res_roi)


def test_privacy_filter_blank_image():
    filter_obj = PrivacyFilter()

    img = Image.new("RGB", (400, 300), color=(128, 128, 128))
    result = filter_obj.redact_sensitive_data(img)

    assert isinstance(result, Image.Image)
    assert result.size == (400, 300)
    assert result.mode == "RGB"
