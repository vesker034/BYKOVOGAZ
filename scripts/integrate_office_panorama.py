"""Копирует панораму тура в static/tours/office-tour/panorama/."""
from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "static" / "tours" / "office-tour" / "panorama"
ASSETS = Path(r"C:\Users\andre\.cursor\projects\c-Users-andre-OneDrive-2026\assets")
PANORAMA_OUT = OUT_DIR / "office.jpg"
MAX_WIDTH = 4096
JPEG_QUALITY = 88

# Последняя загруженная панорама (equirectangular)
SOURCE_GLOB = "*images_photo_1_*3fbe774e*.png"


def _find_source() -> Path:
    matches = sorted(ASSETS.glob(SOURCE_GLOB), key=lambda p: p.stat().st_mtime, reverse=True)
    if not matches:
        matches = sorted(ASSETS.glob("*images_photo_1*.png"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not matches:
        raise SystemExit(f"Panorama not found in {ASSETS}")
    return matches[0]


def main() -> None:
    src = _find_source()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with Image.open(src) as im:
        im = im.convert("RGB")
        w, h = im.size
        if w > MAX_WIDTH:
            nh = int(h * MAX_WIDTH / w)
            im = im.resize((MAX_WIDTH, nh), Image.Resampling.LANCZOS)
        im.save(PANORAMA_OUT, "JPEG", quality=JPEG_QUALITY, optimize=True)
        print(f"OK: {src.name} -> {PANORAMA_OUT} ({im.size[0]}x{im.size[1]})")


if __name__ == "__main__":
    main()
