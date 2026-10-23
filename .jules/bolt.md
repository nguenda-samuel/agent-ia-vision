## 2025-02-23 - OpenCV Color Conversions in Privacy Pipelines
**Learning:** Converting RGB PIL images to BGR format solely to extract grayscale images and then converting back to RGB before returning adds ~12-15ms of overhead per frame on standard 1080p images.
**Action:** Use `cv2.COLOR_RGB2GRAY` directly on the numpy array derived from PIL images, and perform spatial filtering (e.g. GaussianBlur) directly on the RGB array without intermediate BGR transformations.
