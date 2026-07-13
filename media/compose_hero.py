#!/usr/bin/env python
"""Compose exact typography over the GPT Image 2 cover source."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "media" / "source" / "hero-base-gpt-image-2.png"
OUTPUT = ROOT / "media" / "exports" / "article-cover.png"
WIDTH, HEIGHT = 1600, 900
WHITE = "#F2F0E9"
MUTED = "#9AA6AE"
ACCENT = "#42F59E"


def cover_resize(image: Image.Image) -> Image.Image:
    source_ratio = image.width / image.height
    target_ratio = WIDTH / HEIGHT
    if source_ratio > target_ratio:
        new_height = HEIGHT
        new_width = round(HEIGHT * source_ratio)
    else:
        new_width = WIDTH
        new_height = round(WIDTH / source_ratio)
    resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    left = (new_width - WIDTH) // 2
    top = (new_height - HEIGHT) // 2
    return resized.crop((left, top, left + WIDTH, top + HEIGHT))


def main() -> None:
    with Image.open(SOURCE) as source:
        base = cover_resize(source.convert("RGB")).convert("RGBA")

    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    pixels = overlay.load()
    for y in range(HEIGHT):
        top_alpha = max(0, int(225 * (1 - y / 430))) if y < 430 else 0
        for x in range(WIDTH):
            left_alpha = max(0, int(105 * (1 - x / 850))) if x < 850 else 0
            alpha = min(235, top_alpha + left_alpha - (top_alpha * left_alpha // 255))
            pixels[x, y] = (7, 9, 11, alpha)
    base = Image.alpha_composite(base, overlay)

    draw = ImageDraw.Draw(base)
    font_root = Path(r"C:\Windows\Fonts")
    label = ImageFont.truetype(str(font_root / "consola.ttf"), 22)
    title = ImageFont.truetype(str(font_root / "segoeuib.ttf"), 66)
    title_accent = ImageFont.truetype(str(font_root / "segoeuib.ttf"), 74)
    subtitle = ImageFont.truetype(str(font_root / "segoeui.ttf"), 27)
    footer = ImageFont.truetype(str(font_root / "consola.ttf"), 20)

    draw.text((78, 60), "VIBES TO VERIFIED / AGENT VERIFICATION", font=label, fill=ACCENT)
    draw.text((75, 112), "vibe coding isn't the problem.", font=title, fill=WHITE)
    draw.text((75, 192), "stopping at vibes is.", font=title_accent, fill=ACCENT)
    draw.text(
        (78, 292),
        "a five-level system for turning AI-generated work into verified evidence",
        font=subtitle,
        fill=MUTED,
    )
    footer_text = "MAKE YOUR AGENTS PROVE IT."
    box = draw.textbbox((0, 0), footer_text, font=footer)
    draw.text((WIDTH - (box[2] - box[0]) - 55, HEIGHT - 55), footer_text, font=footer, fill=ACCENT)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    base.convert("RGB").save(OUTPUT, quality=96, optimize=True)
    print(f"wrote {OUTPUT} {OUTPUT.stat().st_size} bytes")


if __name__ == "__main__":
    main()
