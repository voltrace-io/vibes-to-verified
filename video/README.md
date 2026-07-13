# Manim Video

The launch animation is native Manim and contains no generated text or simulated interface footage.

## Verified Render Environment

- Manim Community `0.20.1`
- Python `3.14.6`
- FFmpeg `8.1.2`
- Output: H.264, 1080 × 1920, 30 fps
- Measured duration: 28.664 seconds

## Render

With Manim and FFmpeg available:

```bash
python -m manim -ql --disable_caching video/vibes_to_verified.py VibesToVerified
```

The scene itself pins the production dimensions and frame rate. Manim writes its normal intermediate tree under `media/videos/`; the verified final export is committed at:

```text
media/exports/vibes-to-verified-vertical.mp4
```

## QA

The final export was checked with `ffprobe`, sampled into a contact sheet, inspected frame by frame, and reviewed as a complete muted video. The full-motion review returned PASS with no blocking visual defect.

See [`plan.md`](plan.md) for the narrative and acceptance criteria.
