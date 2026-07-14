# Launch Videos

The package contains two complementary 9:16 videos.

## Narrated Motion Launch Cut

Public launch asset:

```text
media/exports/vibes-to-verified-launch-cut-r1.mp4
```

Verified properties:

- H.264 video, AAC stereo audio
- 1080 × 1920
- 30 fps
- 28.665 seconds
- SHA-256: `f067ebb462e545d4a4bad3750cc098cc639258d189085e7fa8c6a5f30a76150e`

The launch cut combines locally generated text-free LTX-2.3 motion plates, authored typography and diagrams, the creator's narration, and a music track the creator reports as cleared for this publication. The private rights receipt is withheld. Embedded narration and music are excluded from the repository's MIT grant and are not licensed for standalone reuse; see [`../media/RIGHTS.md`](../media/RIGHTS.md). The public package includes the final rendered artifact, not the private voice reference, generated plates, keyframes, or production workspace.

Technical QC established a complete decode, no detected black/frozen/silent intervals, and exact AAC packet-hash equality with the approved audio master. A 2 fps disclosure contact sheet and transcript scan found no visible or audible private paths, credentials, account data, contact details, or personal identifiers. The automated full-video analysis backend could not ingest the local file, so the disclosure review used sampled-frame inspection plus exact-audio transcription rather than that backend.

## Deterministic Muted Manim Overview

Reproducible public source:

```text
video/vibes_to_verified.py
```

Render with Manim Community 0.20.1 and FFmpeg:

```bash
python -m manim -ql --disable_caching video/vibes_to_verified.py VibesToVerified
```

Verified export:

```text
media/exports/vibes-to-verified-vertical.mp4
```

Properties:

- H.264
- 1080 × 1920
- 30 fps
- 28.664 seconds
- Muted

The scene pins production dimensions and frame rate. Manim writes intermediates under `media/videos/`, which remains excluded from the release.

See [`plan.md`](plan.md) for the narrative and acceptance criteria.
