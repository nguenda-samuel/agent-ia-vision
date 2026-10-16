## 2026-10-16 - Direct RGB Processing in OpenCV Privacy Filter
**Learning:** In PIL/OpenCV image pipelines, converting PIL RGB array to BGR solely for OpenCV operations and converting back to RGB before returning PIL Image adds unnecessary full-frame color conversion overhead. OpenCV functions like `cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)` and channel-wise `cv2.GaussianBlur` work directly on RGB arrays.
**Action:** When processing PIL images in OpenCV, convert directly from RGB to GRAY and operate in-place on the RGB array, avoiding redundant `RGB2BGR` and `BGR2RGB` passes.
