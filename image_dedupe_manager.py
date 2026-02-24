#!/usr/bin/env python3
"""Image duplicate manager with a local app recycle bin.

Features
- Exact duplicate detection via SHA-256.
- Optional visual duplicate detection via perceptual hash.
- Safety guards for visual mode: do not delete when dimensions or DPI differ.
- Quarantine delete candidates into an app-managed recycle bin.
- Restore files from the app recycle bin.
- Optional purge from app recycle bin to Windows recycle bin or permanent delete.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

from PIL import Image
import imagehash

try:
    from send2trash import send2trash
except Exception:  # pragma: no cover - optional dependency fallback
    send2trash = None

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".bmp",
    ".gif",
    ".tif",
    ".tiff",
    ".heic",
    ".heif",
}


@dataclass
class ImageMeta:
    path: Path
    mtime: float
    size_bytes: int
    width: int
    height: int
    dpi_x: Optional[float]
    dpi_y: Optional[float]
    sha256: str
    phash: Optional[imagehash.ImageHash]


def iter_images(roots: Sequence[Path]) -> Iterable[Path]:
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS:
                yield path


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def read_meta(path: Path, include_visual_hash: bool) -> Optional[ImageMeta]:
    stat = path.stat()
    width = 0
    height = 0
    dpi_x: Optional[float] = None
    dpi_y: Optional[float] = None
    phash: Optional[imagehash.ImageHash] = None

    try:
        with Image.open(path) as img:
            width, height = img.size
            raw_dpi = img.info.get("dpi")
            if isinstance(raw_dpi, tuple) and len(raw_dpi) >= 2:
                dpi_x = float(raw_dpi[0])
                dpi_y = float(raw_dpi[1])
            elif isinstance(raw_dpi, (int, float)):
                dpi_x = float(raw_dpi)
                dpi_y = float(raw_dpi)
            if include_visual_hash:
                phash = imagehash.phash(img)
    except Exception:
        return None

    return ImageMeta(
        path=path,
        mtime=stat.st_mtime,
        size_bytes=stat.st_size,
        width=width,
        height=height,
        dpi_x=dpi_x,
        dpi_y=dpi_y,
        sha256=sha256_file(path),
        phash=phash,
    )


def choose_keep_newest(members: Sequence[ImageMeta]) -> ImageMeta:
    return sorted(
        members,
        key=lambda m: (m.mtime, m.size_bytes, str(m.path).lower()),
        reverse=True,
    )[0]


def same_dimensions_and_dpi(a: ImageMeta, b: ImageMeta) -> bool:
    if (a.width, a.height) != (b.width, b.height):
        return False

    if a.dpi_x is None or a.dpi_y is None or b.dpi_x is None or b.dpi_y is None:
        return a.dpi_x is None and a.dpi_y is None and b.dpi_x is None and b.dpi_y is None

    return round(a.dpi_x, 2) == round(b.dpi_x, 2) and round(a.dpi_y, 2) == round(b.dpi_y, 2)


def ensure_run_bin(base_bin: Path) -> Path:
    run_bin = base_bin / datetime.now().strftime("%Y%m%d_%H%M%S")
    run_bin.mkdir(parents=True, exist_ok=True)
    return run_bin


def safe_relpath(path: Path) -> str:
    drive = path.drive.replace(":", "") if path.drive else "root"
    without_anchor = Path(*path.parts[1:]) if path.is_absolute() and len(path.parts) > 1 else path
    return str(Path(drive) / without_anchor)


def move_to_app_bin(meta: ImageMeta, run_bin: Path) -> Path:
    rel = safe_relpath(meta.path)
    destination = run_bin / rel
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(meta.path), str(destination))
    return destination


def write_manifest(manifest_path: Path, rows: List[Dict[str, object]]) -> None:
    with manifest_path.open("a", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def dedupe(
    source_dirs: Sequence[Path],
    app_bin: Path,
    include_visual: bool,
    visual_distance: int,
    dry_run: bool,
) -> Dict[str, int]:
    metas: List[ImageMeta] = []
    for img_path in iter_images(source_dirs):
        meta = read_meta(img_path, include_visual_hash=include_visual)
        if meta:
            metas.append(meta)

    stats = {
        "scanned": len(metas),
        "exact_groups": 0,
        "visual_groups": 0,
        "moved": 0,
        "protected": 0,
    }

    by_sha: Dict[str, List[ImageMeta]] = {}
    for meta in metas:
        by_sha.setdefault(meta.sha256, []).append(meta)

    duplicate_rows: List[Dict[str, object]] = []
    run_bin = ensure_run_bin(app_bin) if not dry_run else app_bin / "DRY_RUN"
    manifest_path = run_bin / "manifest.jsonl"

    removed_paths: set[Path] = set()

    for group in by_sha.values():
        if len(group) < 2:
            continue
        stats["exact_groups"] += 1
        keep = choose_keep_newest(group)
        for candidate in group:
            if candidate.path == keep.path:
                continue
            removed_paths.add(candidate.path)
            if not dry_run:
                moved_to = move_to_app_bin(candidate, run_bin)
                stats["moved"] += 1
                duplicate_rows.append(
                    {
                        "reason": "exact_duplicate",
                        "kept": str(keep.path),
                        "removed": str(candidate.path),
                        "stored_in_app_bin": str(moved_to),
                        "sha256": candidate.sha256,
                        "width": candidate.width,
                        "height": candidate.height,
                        "dpi": [candidate.dpi_x, candidate.dpi_y],
                        "timestamp": datetime.utcnow().isoformat() + "Z",
                    }
                )

    if include_visual:
        remaining = [m for m in metas if m.path not in removed_paths and m.phash is not None]
        remaining_sorted = sorted(remaining, key=lambda m: m.mtime, reverse=True)
        seen: set[Path] = set()

        for i, anchor in enumerate(remaining_sorted):
            if anchor.path in seen:
                continue
            group = [anchor]
            for other in remaining_sorted[i + 1 :]:
                if other.path in seen:
                    continue
                if other.phash is None or anchor.phash is None:
                    continue
                if anchor.phash - other.phash <= visual_distance:
                    group.append(other)
            if len(group) < 2:
                continue

            stats["visual_groups"] += 1
            keep = choose_keep_newest(group)
            for candidate in group:
                seen.add(candidate.path)
                if candidate.path == keep.path:
                    continue
                if not same_dimensions_and_dpi(keep, candidate):
                    stats["protected"] += 1
                    continue
                if not dry_run:
                    moved_to = move_to_app_bin(candidate, run_bin)
                    stats["moved"] += 1
                    duplicate_rows.append(
                        {
                            "reason": "visual_duplicate",
                            "kept": str(keep.path),
                            "removed": str(candidate.path),
                            "stored_in_app_bin": str(moved_to),
                            "phash_keep": str(keep.phash),
                            "phash_removed": str(candidate.phash),
                            "width": candidate.width,
                            "height": candidate.height,
                            "dpi": [candidate.dpi_x, candidate.dpi_y],
                            "timestamp": datetime.utcnow().isoformat() + "Z",
                        }
                    )

    if duplicate_rows and not dry_run:
        write_manifest(manifest_path, duplicate_rows)

    return stats


def restore_from_app_bin(app_bin: Path) -> int:
    restored = 0
    manifests = sorted(app_bin.glob("*/manifest.jsonl"))
    for manifest in manifests:
        with manifest.open("r", encoding="utf-8") as f:
            rows = [json.loads(line) for line in f if line.strip()]

        for row in reversed(rows):
            stored = Path(row["stored_in_app_bin"])
            original = Path(row["removed"])
            if stored.exists():
                original.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(stored), str(original))
                restored += 1
    return restored


def purge_app_bin(app_bin: Path, mode: str) -> int:
    purged = 0
    for run_dir in sorted(p for p in app_bin.glob("*") if p.is_dir()):
        for file in run_dir.rglob("*"):
            if not file.is_file() or file.name == "manifest.jsonl":
                continue
            if mode == "recycle":
                if send2trash is None:
                    raise RuntimeError("send2trash is not installed. Install it to use recycle mode.")
                send2trash(str(file))
            elif mode == "permanent":
                file.unlink(missing_ok=True)
            purged += 1
        shutil.rmtree(run_dir, ignore_errors=True)
    return purged


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Image duplicate manager with app recycle bin")
    sub = p.add_subparsers(dest="command", required=True)

    scan = sub.add_parser("scan", help="Find duplicates and move old versions to app recycle bin")
    scan.add_argument("--source", nargs="+", required=True, help="One or more source folders to scan")
    scan.add_argument(
        "--app-bin",
        default="./app_recycle_bin",
        help="Folder used as app-managed recycle bin",
    )
    scan.add_argument(
        "--visual",
        action="store_true",
        help="Enable visual duplicate mode (protected by same dimensions and DPI rule)",
    )
    scan.add_argument(
        "--visual-distance",
        type=int,
        default=2,
        help="pHash distance threshold for visual matching (lower is stricter)",
    )
    scan.add_argument("--dry-run", action="store_true", help="Only report stats, do not move files")

    restore = sub.add_parser("restore", help="Restore files from app recycle bin to original paths")
    restore.add_argument("--app-bin", default="./app_recycle_bin")

    purge = sub.add_parser(
        "purge",
        help="Purge files currently in app recycle bin to Windows recycle bin or permanently",
    )
    purge.add_argument("--app-bin", default="./app_recycle_bin")
    purge.add_argument("--mode", choices=["recycle", "permanent"], default="recycle")

    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "scan":
        stats = dedupe(
            source_dirs=[Path(s).expanduser().resolve() for s in args.source],
            app_bin=Path(args.app_bin).expanduser().resolve(),
            include_visual=args.visual,
            visual_distance=args.visual_distance,
            dry_run=args.dry_run,
        )
        print(json.dumps(stats, indent=2))
        return 0

    if args.command == "restore":
        restored = restore_from_app_bin(Path(args.app_bin).expanduser().resolve())
        print(json.dumps({"restored": restored}, indent=2))
        return 0

    if args.command == "purge":
        purged = purge_app_bin(Path(args.app_bin).expanduser().resolve(), mode=args.mode)
        print(json.dumps({"purged": purged, "mode": args.mode}, indent=2))
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
