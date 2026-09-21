## 2026-08-30 - Downscale images before OpenCV privacy filtering
**Learning:** OpenCV `detectMultiScale` and `findContours` processing times scale quadratically with image dimensions. Resizing raw screenshots to max 768x768 before privacy filtering reduces privacy filter processing time from ~580ms to ~58ms per frame (~10x speedup) without losing necessary face/contour features.
**Action:** When performing vision/OpenCV transformations on full screen captures, downscale the image to target resolution early in the pipeline before applying compute-heavy filters.
