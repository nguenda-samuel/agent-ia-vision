import numpy as np
from PIL import Image
from privacy import PrivacyFilter


def test_redact_sensitive_data_dimensions_and_mode():
    pf = PrivacyFilter()
    # Create a test image
    img = Image.new("RGB", (200, 200), color=(128, 128, 128))
    result = pf.redact_sensitive_data(img)

    assert isinstance(result, Image.Image)
    assert result.size == (200, 200)
    assert result.mode == "RGB"


def test_redact_sensitive_data_preserves_colors():
    pf = PrivacyFilter()
    # Create a simple red image (200x200) with no features to blur
    img = Image.new("RGB", (200, 200), color=(255, 0, 0))
    result = pf.redact_sensitive_data(img)

    result_arr = np.array(result)
    # Ensure red channel is predominant and green/blue channels are 0
    assert np.all(result_arr[:, :, 0] == 255)
    assert np.all(result_arr[:, :, 1] == 0)
    assert np.all(result_arr[:, :, 2] == 0)
