## 2026-10-01 - Avoid Redundant Full-Frame Image Color Conversions in OpenCV/PIL Pipelines

**Learning:** Converting full-resolution images back and forth between color spaces (e.g., RGB to BGR and BGR back to RGB) in PIL/OpenCV privacy and vision pipelines adds significant CPU overhead and array buffer allocations (~28 ms per 1080p frame). OpenCV functions like `cv2.COLOR_RGB2GRAY` convert directly from RGB, and ROI modifications (such as `cv2.GaussianBlur`) operate channel-wise on numpy slices identically regardless of color order.

**Action:** Keep numpy image arrays in their native RGB representation, convert directly to grayscale for feature/face detection, and apply spatial filters (blur, redact) directly in RGB space to avoid round-trip `COLOR_RGB2BGR` / `COLOR_BGR2RGB` conversions.
