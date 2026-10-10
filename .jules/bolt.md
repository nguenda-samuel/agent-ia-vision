## 2025-02-16 - Eliminate Redundant Color Space Conversions in Frame Redaction
**Learning:** OpenCV operations like `cv2.GaussianBlur` operate independently on each image channel regardless of whether the color order is RGB or BGR. Converting PIL RGB arrays to BGR and back before/after grayscale conversion and blurring added ~15ms unnecessary overhead per 1080p frame.
**Action:** When working with PIL images and OpenCV filters/detectors, convert RGB directly to Grayscale (`cv2.COLOR_RGB2GRAY`) and apply channel-agnostic filters directly on the RGB array to eliminate double color conversions.
