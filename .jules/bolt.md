# Bolt's Journal

## 2026-08-30 - Eliminating Redundant Color Space Conversions in Vision Pipeline
**Learning:** In computer vision pipelines receiving PIL RGB images (such as screen captures), converting `RGB -> BGR` simply to perform Haar cascade face detection and Gaussian blurring on ROIs wastes ~4.5ms per 1080p frame and allocates multiple large NumPy frame buffers. Grayscale conversion can be performed directly from RGB (`cv2.COLOR_RGB2GRAY`), and spatial convolution operations like `cv2.GaussianBlur` are channel-independent.
**Action:** When integrating PIL and OpenCV for image filtering or redacting, keep the buffer in its native channel order (RGB) and convert directly to Grayscale (`cv2.COLOR_RGB2GRAY`), avoiding intermediate `cv2.COLOR_RGB2BGR` and `cv2.COLOR_BGR2RGB` passes.
