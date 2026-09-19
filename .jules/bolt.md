## 2026-03-31 - Direct RGB Processing in OpenCV / PIL Pipelines

**Learning:** When using PIL images with OpenCV, converting `RGB -> BGR` before grayscale conversion or channel-independent operations like `GaussianBlur` introduces redundant full-image array conversions and copies. OpenCV supports direct `RGB -> Grayscale` conversion via `cv2.COLOR_RGB2GRAY`, and Gaussian blur operates identically on RGB or BGR channels.
**Action:** Avoid round-trip `RGB -> BGR -> RGB` conversions in OpenCV image preprocessing pipelines when operations (like channel-wise blur or thresholding) are color-space agnostic.
