## 2025-02-18 - Avoid Redundant OpenCV BGR Conversions on PIL Images

**Learning:** PIL Images converted to NumPy arrays are in RGB format by default. Converting the entire frame to BGR (`cv2.COLOR_RGB2BGR`) before Grayscale conversion (`cv2.COLOR_BGR2GRAY`) and back to RGB (`cv2.COLOR_BGR2RGB`) at the end introduces unnecessary full-array copies and channel swaps. OpenCV detection algorithms require Grayscale, which can be computed directly from RGB (`cv2.COLOR_RGB2GRAY`), and region operations like `cv2.GaussianBlur` work on RGB array slices identically to BGR.

**Action:** Convert PIL NumPy arrays directly from RGB to Grayscale for detection tasks, and perform OpenCV spatial modifications (like blurs) directly on the RGB array to avoid double full-frame color space conversions.
