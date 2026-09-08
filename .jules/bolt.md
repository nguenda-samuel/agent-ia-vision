## 2026-09-08 - Avoid redundant OpenCV color space conversions for invariant operations

**Learning:** `PrivacyFilter.redact_sensitive_data` was converting PIL RGB images to BGR (`COLOR_RGB2BGR`) before converting to Grayscale (`COLOR_BGR2GRAY`), and then converting back from BGR to RGB (`COLOR_BGR2RGB`). OpenCV operations like Gaussian blur on image regions work on channel slices independently and produce identical results regardless of channel ordering (RGB vs BGR). Eliminating the intermediate BGR roundtrips avoids allocating 2 full-resolution frame image copies per screenshot.

**Action:** Convert PIL RGB NumPy arrays directly to grayscale via `cv2.COLOR_RGB2GRAY` and perform channel-agnostic operations (like blurring or thresholding) directly on the RGB array.
