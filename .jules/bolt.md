## 2026-09-15 - Redundant Color Space Conversions in PIL-to-OpenCV Pipelines

**Learning:** When passing PIL images (which use RGB color format) to OpenCV for processing such as grayscale conversion and `cv2.GaussianBlur`, converting the NumPy array to BGR (`cv2.COLOR_RGB2BGR`) before converting to grayscale (`cv2.COLOR_BGR2GRAY`) and back (`cv2.COLOR_BGR2RGB`) is completely redundant. `cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)` converts directly from RGB to Grayscale, and OpenCV's `GaussianBlur` operates directly on RGB slice arrays without color distortion.

**Action:** Convert PIL RGB arrays directly to grayscale via `cv2.COLOR_RGB2GRAY` and operate on the RGB array directly to eliminate unnecessary frame copies and color conversions.
