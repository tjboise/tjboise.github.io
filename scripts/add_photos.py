"""Resize photos, make thumbnails, and update the per-year gallery JSON.

Usage:
    python scripts/add_photos.py photos-src            # every image in the folder
    python scripts/add_photos.py photos-src --max 2400 # longest side of the full image

Output (the year comes from EXIF DateTimeOriginal, else the file's modified time):
    static/images/photography/<date>-<name>.jpg
    static/images/photography/<date>-<name>-thumbnail.jpg
    static/data/photography/<year>.json
"""

import argparse
import json
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
IMAGE_DIR = ROOT / "static" / "images" / "photography"
DATA_DIR = ROOT / "static" / "data" / "photography"
EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff"}

GALLERY_OPTIONS = {
    "justifiedGalleryOptions": {
        "rowHeight": 160,
        "maxRowHeight": 320,
        "captions": True,
        "captionSettings": {
            "animationDuration": 400,
            "visibleOpacity": 0.8,
            "nonVisibleOpacity": 0.0,
        },
        "cssAnimation": False,
        "lastRow": "justify",
        "margins": 6,
    },
    "lightGalleryOptions": {
        "autoplayFirstVideo": False,
        "iframeMaxHeight": "90%",
        "iframeMaxWidth": "30%",
    },
}


def shot_date(path: Path, image: Image.Image) -> datetime:
    exif = image.getexif()
    raw = exif.get_ifd(0x8769).get(36867) or exif.get(306)  # DateTimeOriginal, DateTime
    if raw:
        try:
            return datetime.strptime(str(raw), "%Y:%m:%d %H:%M:%S")
        except ValueError:
            pass
    return datetime.fromtimestamp(path.stat().st_mtime)


def load_items(year: str) -> list[dict]:
    path = DATA_DIR / f"{year}.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8")).get("items", [])
    return []


def save_items(year: str, items: list[dict]) -> None:
    items.sort(key=lambda item: item["src"])
    data = {**GALLERY_OPTIONS, "items": items}
    (DATA_DIR / f"{year}.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("source", type=Path, help="folder holding the original photos")
    parser.add_argument("--max", type=int, default=2400, help="longest side of the full image")
    parser.add_argument("--thumb", type=int, default=320, help="thumbnail height")
    parser.add_argument("--quality", type=int, default=85)
    args = parser.parse_args()

    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    by_year: dict[str, list[dict]] = {}
    files = sorted(p for p in args.source.rglob("*") if p.suffix.lower() in EXTENSIONS)
    if not files:
        raise SystemExit(f"no images found in {args.source}")

    for path in files:
        with Image.open(path) as opened:
            image = ImageOps.exif_transpose(opened).convert("RGB")
            taken = shot_date(path, opened)

        name = f"{taken:%Y-%m-%d}-{path.stem.lower().replace(' ', '-')}"
        full = image.copy()
        full.thumbnail((args.max, args.max))
        full.save(IMAGE_DIR / f"{name}.jpg", quality=args.quality, optimize=True)

        thumb = image.copy()
        thumb.thumbnail((10_000, args.thumb))
        thumb.save(IMAGE_DIR / f"{name}-thumbnail.jpg", quality=80, optimize=True)

        year = f"{taken:%Y}"
        if year not in by_year:
            by_year[year] = load_items(year)
        src = f"/images/photography/{name}.jpg"
        by_year[year] = [item for item in by_year[year] if item["src"] != src]
        by_year[year].append(
            {
                "alt": path.stem,
                "download": f"{path.stem}.jpg",
                "src": src,
                "thumb": f"/images/photography/{name}-thumbnail.jpg",
            }
        )
        print(f"{path.name} -> {name}.jpg")

    for year, items in by_year.items():
        save_items(year, items)
        print(f"{year}.json: {len(items)} photos")


if __name__ == "__main__":
    main()
