"""
Подготовка фото-тура офиса: копирование исходников, ресайз, tour.json.
Исходники: PNG в каталоге Cursor assets (*images_photo_*2026-06-02_23-57-54*).
"""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "static" / "tours" / "office-tour"
IMAGES = OUT / "images"
ASSETS = Path(r"C:\Users\andre\.cursor\projects\c-Users-andre-OneDrive-2026\assets")
PHOTO_GLOB = "*images_photo_*2026-06-02_23-57-54*.png"
MAX_EDGE = 1920
JPEG_QUALITY = 85

# slug -> (filename_substring hints для авто-раскладки, заголовок)
ZONES = {
    "workspace": (
        ("window", "окно", "вид"),
        "Офисное пространство",
    ),
    "meeting": (
        ("flipchart", "cooler", "кулер", "plant"),
        "Общая зона",
    ),
    "server": (
        ("printer", "tower", "cooler master", "router", "msi"),
        "Рабочие места и техника",
    ),
}

# Ручной приоритет: лучшие кадры без зеркальных селфи (по номеру в имени photo_N)
PREFERRED_ORDER = [
    24, 18, 13, 7, 6, 20, 2, 11, 23, 16, 17, 14, 8, 12, 4, 22, 21, 3,
    25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
]


def _photo_num(path: Path) -> int | None:
    m = re.search(r"images_photo_(\d+)_", path.name)
    return int(m.group(1)) if m else None


def _collect_sources() -> list[Path]:
    files = sorted(ASSETS.glob(PHOTO_GLOB), key=lambda p: _photo_num(p) or 0)
    if not files:
        raise SystemExit(f"Не найдены фото в {ASSETS}")
    by_num = {_photo_num(p): p for p in files if _photo_num(p) is not None}
    ordered: list[Path] = []
    seen: set[Path] = set()
    for n in PREFERRED_ORDER:
        if n in by_num and by_num[n] not in seen:
            ordered.append(by_num[n])
            seen.add(by_num[n])
    for p in files:
        if p not in seen:
            ordered.append(p)
            seen.add(p)
    return ordered[:18]


def _resize_save(src: Path, dest: Path) -> tuple[int, int]:
    with Image.open(src) as im:
        im = im.convert("RGB")
        w, h = im.size
        scale = min(1.0, MAX_EDGE / max(w, h))
        if scale < 1.0:
            im = im.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)
        im.save(dest, "JPEG", quality=JPEG_QUALITY, optimize=True)
        return im.size


def _guess_zone(path: Path, index: int) -> str:
    # Равномерное распределение по трём зонам сайта
    keys = list(ZONES.keys())
    return keys[index % len(keys)]


def main() -> None:
    if IMAGES.exists():
        shutil.rmtree(IMAGES)
    IMAGES.mkdir(parents=True)

    sources = _collect_sources()
    scenes = []
    for i, src in enumerate(sources, start=1):
        name = f"scene-{i:02d}.jpg"
        dest = IMAGES / name
        w, h = _resize_save(src, dest)
        zone = _guess_zone(src, i - 1)
        title = ZONES[zone][1]
        if i <= 6:
            subtitles = [
                "Рабочие места у окна",
                "Зона отдыха и воды",
                "Кабинеты сотрудников",
                "Проход и смежные помещения",
                "Организация рабочих мест",
                "Общий вид open space",
            ]
            title = subtitles[min(i - 1, len(subtitles) - 1)]
        scenes.append(
            {
                "id": f"scene-{i:02d}",
                "zone": zone,
                "title": title,
                "image": f"images/{name}",
                "width": w,
                "height": h,
            },
        )

    tour = {
        "version": 1,
        "kind": "photo-walkthrough",
        "start": scenes[0]["id"],
        "scenes": scenes,
    }
    (OUT / "tour.json").write_text(
        json.dumps(tour, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"OK: {len(scenes)} scenes in {OUT}")


if __name__ == "__main__":
    main()
