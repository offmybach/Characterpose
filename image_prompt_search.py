#!/usr/bin/env python3
"""Prompt-based local image search tool.

Primary goal:
- Index images from one or more folders.
- Search by natural language prompt ("pile of newspaper", "blue and white shoes").
- Return best matching file paths by semantic similarity.

This tool stores a local index in a folder (default: ./.image_search_index).
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable, List, Sequence

import numpy as np
from PIL import Image
from sentence_transformers import SentenceTransformer

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif", ".tif", ".tiff", ".heic", ".heif"}


@dataclass
class ImageRecord:
    path: str
    width: int
    height: int
    mtime: float


def iter_images(roots: Sequence[Path]) -> Iterable[Path]:
    for root in roots:
        if not root.exists():
            continue
        for dirpath, _, filenames in os.walk(root, onerror=lambda _: None):
            for filename in filenames:
                suffix = Path(filename).suffix.lower()
                if suffix in IMAGE_EXTENSIONS:
                    yield Path(dirpath) / filename


def source_scan_summary(source_dirs: Sequence[Path]) -> list[dict]:
    summary: list[dict] = []
    for src in source_dirs:
        src_path = Path(src)
        row = {
            "source": str(src_path),
            "exists": src_path.exists(),
            "candidate_images": 0,
        }
        if src_path.exists():
            row["candidate_images"] = sum(1 for _ in iter_images([src_path]))
        summary.append(row)
    return summary


def load_model(model_name: str) -> SentenceTransformer:
    return SentenceTransformer(model_name)


def normalize(vectors: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return vectors / norms


def build_index(source_dirs: Sequence[Path], index_dir: Path, model_name: str, batch_size: int = 16) -> dict:
    model = load_model(model_name)
    scan = source_scan_summary(source_dirs)
    print(json.dumps({"scan_summary": scan}, indent=2))
    image_paths = list(iter_images(source_dirs))

    records: List[ImageRecord] = []
    pil_images: List[Image.Image] = []

    for p in image_paths:
        try:
            with Image.open(p) as img:
                width, height = img.size
                pil_images.append(img.convert("RGB"))
            records.append(ImageRecord(path=str(p), width=width, height=height, mtime=p.stat().st_mtime))
        except Exception:
            continue

    if not records:
        raise RuntimeError(
            "No readable images found in provided source folders. "
            "Check scan_summary above for missing paths or zero candidate images. "
            "Tip: point to folders that definitely contain supported image types "
            f"({', '.join(sorted(IMAGE_EXTENSIONS))})."
        )

    embeddings = model.encode(pil_images, batch_size=batch_size, convert_to_numpy=True, show_progress_bar=True)
    embeddings = normalize(embeddings.astype(np.float32))

    index_dir.mkdir(parents=True, exist_ok=True)
    np.save(index_dir / "embeddings.npy", embeddings)

    with (index_dir / "metadata.jsonl").open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(asdict(r), ensure_ascii=False) + "\n")

    with (index_dir / "index_config.json").open("w", encoding="utf-8") as f:
        json.dump({"model": model_name, "count": len(records)}, f, indent=2)

    return {"indexed": len(records), "index_dir": str(index_dir), "model": model_name}


def load_index(index_dir: Path) -> tuple[np.ndarray, List[ImageRecord], str]:
    cfg = json.loads((index_dir / "index_config.json").read_text(encoding="utf-8"))
    model_name = cfg["model"]
    embeddings = np.load(index_dir / "embeddings.npy")

    records: List[ImageRecord] = []
    with (index_dir / "metadata.jsonl").open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                row = json.loads(line)
                records.append(ImageRecord(**row))

    if len(records) != embeddings.shape[0]:
        raise RuntimeError("Index files are inconsistent (metadata count != embedding count).")

    return embeddings, records, model_name


def search(index_dir: Path, query: str, top_k: int = 30) -> list[dict]:
    embeddings, records, model_name = load_index(index_dir)
    model = load_model(model_name)

    q = model.encode([query], convert_to_numpy=True).astype(np.float32)
    q = normalize(q)

    scores = embeddings @ q[0]
    order = np.argsort(-scores)[:top_k]

    results = []
    for i in order:
        rec = records[int(i)]
        results.append(
            {
                "path": rec.path,
                "score": float(scores[i]),
                "width": rec.width,
                "height": rec.height,
            }
        )
    return results


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Prompt-based local image search")
    sub = p.add_subparsers(dest="command", required=True)

    index = sub.add_parser("index", help="Build (or rebuild) local image search index")
    index.add_argument("--source", nargs="+", required=True, help="Folders to scan for images")
    index.add_argument("--index-dir", default="./.image_search_index", help="Where to store index files")
    index.add_argument("--model", default="clip-ViT-B-32", help="SentenceTransformer model name")
    index.add_argument("--batch-size", type=int, default=16)

    find = sub.add_parser("search", help="Search indexed images by text prompt")
    find.add_argument("--index-dir", default="./.image_search_index")
    find.add_argument("--query", required=True, help="Text query, e.g. 'pile of newspaper'")
    find.add_argument("--top-k", type=int, default=30)

    return p


def normalize_source_path(raw: str) -> Path:
    s = raw.strip().strip('"').strip("'")
    # Treat bare drive letters as roots on Windows ("C:" -> "C:\\").
    if len(s) == 2 and s[1] == ":":
        s = s + "\\"
    return Path(s).expanduser().resolve()


def main() -> int:
    args = parser().parse_args()

    if args.command == "index":
        out = build_index(
            source_dirs=[normalize_source_path(s) for s in args.source],
            index_dir=Path(args.index_dir).expanduser().resolve(),
            model_name=args.model,
            batch_size=args.batch_size,
        )
        print(json.dumps(out, indent=2))
        return 0

    if args.command == "search":
        out = search(
            index_dir=Path(args.index_dir).expanduser().resolve(),
            query=args.query,
            top_k=args.top_k,
        )
        print(json.dumps(out, indent=2))
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
