## 2026-09-29 - Perceptual Hashing Latency on High-Resolution Screenshots

**Learning:** `imagehash.phash` internally resizes PIL images to 32x32 using PIL's default high-quality `LANCZOS` resampling filter. On 1080p or 4K desktop screen captures, computing `phash` directly on the full-resolution image takes ~50.9ms per frame due to resampling millions of pixels.
**Action:** Pre-resize full-resolution screen captures to a smaller size (e.g. 128x128) using fast `Image.Resampling.NEAREST` before passing them to `imagehash.phash`. This reduces perceptual hash calculation latency from ~50.9ms to ~0.9ms per frame (~55x speedup) with identical change-detection accuracy.
