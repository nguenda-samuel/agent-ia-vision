## 2026-03-30 - Direct Grayscale Conversion in Privacy Redaction

**Learning:** PIL images convert directly to NumPy arrays in RGB format (`np.array(pil_image)`). Performing `cv2.cvtColor(img, cv2.COLOR_RGB2BGR)` followed by `cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)` introduces two redundant full-frame color transformations. Since spatial operations like Gaussian blur and face/contour detection operate channel-independently or on grayscale inputs, converting directly with `cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)` and returning `Image.fromarray(open_cv_image)` eliminates ~50% of color space conversion overhead per screen frame.

**Action:** When working with PIL/OpenCV image pipelines, check if color conversions to BGR can be skipped when performing channel-independent spatial filters (like GaussianBlur) or grayscale operations.
