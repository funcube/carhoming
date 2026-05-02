#!/usr/bin/env python3
"""Compress images in a folder: resize to 1200px wide and squeeze under 100KB."""

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageOps

TARGET_WIDTH = 1200
TARGET_BYTES = 100 * 1024
SUPPORTED_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".tif"}


def human_size(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f}{unit}"
        n /= 1024
    return f"{n:.1f}TB"


def resize_to_width(img: Image.Image, width: int) -> Image.Image:
    if img.width <= width:
        return img
    ratio = width / img.width
    return img.resize((width, round(img.height * ratio)), Image.LANCZOS)


def encode_under_target(img: Image.Image, out_path: Path, target_bytes: int) -> int:
    """Save as JPEG; binary-search quality to land under target_bytes.

    Falls back to additional downscaling if quality 30 still overshoots.
    """
    work = img
    while True:
        lo, hi, best = 30, 95, None
        while lo <= hi:
            mid = (lo + hi) // 2
            work.save(out_path, "JPEG", quality=mid, optimize=True, progressive=True)
            size = out_path.stat().st_size
            if size <= target_bytes:
                best = (mid, size)
                lo = mid + 1
            else:
                hi = mid - 1
        if best is not None:
            quality, size = best
            work.save(out_path, "JPEG", quality=quality, optimize=True, progressive=True)
            return size
        new_w = max(400, int(work.width * 0.85))
        if new_w == work.width:
            return out_path.stat().st_size
        work = work.resize((new_w, round(work.height * new_w / work.width)), Image.LANCZOS)


def collect_images(folder: Path) -> list[Path]:
    files = [p for p in sorted(folder.iterdir())
             if p.is_file() and p.suffix.lower() in SUPPORTED_SUFFIXES]
    return files


def compress_folder(folder: Path) -> None:
    if not folder.is_dir():
        sys.exit(f"Not a directory: {folder}")

    images = collect_images(folder)
    if not images:
        print(f"No images found in {folder}")
        return

    out_dir = folder / "WEB"
    out_dir.mkdir(exist_ok=True)

    width = len(str(len(images)))
    width = max(width, 2)
    prefix = folder.name

    total_before = 0
    total_after = 0
    print(f"Processing {len(images)} image(s) from {folder}")
    print(f"Output: {out_dir}")
    print("-" * 72)

    for i, src in enumerate(images, start=1):
        before = src.stat().st_size
        out_name = f"{prefix}_{i:0{width}d}_web.jpg"
        out_path = out_dir / out_name

        with Image.open(src) as im:
            im = ImageOps.exif_transpose(im)
            if im.mode not in ("RGB", "L"):
                im = im.convert("RGB")
            im = resize_to_width(im, TARGET_WIDTH)
            after = encode_under_target(im, out_path, TARGET_BYTES)

        total_before += before
        total_after += after
        flag = "OK" if after <= TARGET_BYTES else "OVER"
        print(f"[{flag}] {src.name:30s} -> {out_name}  "
              f"{human_size(before):>9s} -> {human_size(after):>9s}  "
              f"({after / before * 100:5.1f}%)")

    print("-" * 72)
    saved = total_before - total_after
    pct = (saved / total_before * 100) if total_before else 0
    print(f"Total: {human_size(total_before)} -> {human_size(total_after)}  "
          f"saved {human_size(saved)} ({pct:.1f}%)")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Resize images to 1200px wide and compress under 100KB into a WEB/ subfolder.")
    parser.add_argument("folder", help="Path to the folder containing images")
    args = parser.parse_args()
    compress_folder(Path(args.folder).expanduser().resolve())


if __name__ == "__main__":
    main()
