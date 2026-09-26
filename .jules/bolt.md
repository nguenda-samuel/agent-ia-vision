## 2026-09-26 - Direct RGB to Grayscale Conversion in Vision Processing Pipelines
**Learning:** Converting PIL RGB images to BGR format before computing OpenCV grayscale (`COLOR_BGR2GRAY`) and back to RGB for return creates unnecessary full-resolution frame allocations and color conversion passes. Grayscale detection (`COLOR_RGB2GRAY`) and Gaussian blur operations operate identically on RGB matrices directly.
**Action:** Always process PIL/OpenCV frame buffers in their native color format when applying spatial filters or grayscale detectors, avoiding intermediate color space conversions.
