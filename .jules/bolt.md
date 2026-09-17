## 2026-09-17 - Avoid redundant full-frame color conversions in OpenCV pipelines

**Learning:** When using OpenCV image processing functions (such as `GaussianBlur` or `detectMultiScale`), color conversion from RGB to BGR and back to RGB is unnecessary if operations treat color channels independently or accept direct RGB-to-grayscale conversion (`COLOR_RGB2GRAY`).

**Action:** Directly convert RGB PIL NumPy arrays to grayscale using `COLOR_RGB2GRAY` and return PIL images directly from the modified RGB NumPy array without intermediate BGR transformations.
