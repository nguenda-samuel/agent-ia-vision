## 2025-05-20 - Downsampled Image Analysis for Privacy Filter
**Learning:** Running OpenCV cascade object detection and findContours on full 1080p images is computationally expensive (~150-700ms). Downsampling grayscale inputs by 50% reduces pixel search area by 4x while preserving bounding box detection accuracy, yielding a ~1.7x to 5x latency reduction.
**Action:** Always downsample high-resolution frame inputs before applying feature detection algorithms, then map bounding box ROI coordinates back to full resolution for pixel manipulation.
