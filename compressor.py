# compressor.py
import os
import zipfile
from pathlib import Path
from typing import List, Tuple

def get_file_size_kb(path: Path) -> float:
    return round(path.stat().st_size / 1024, 2)

def should_compress(file_path: Path, size_threshold_kb: float) -> bool:
    if file_path.suffix in {".zip", ".jpg", ".png"}:
        return False
    return get_file_size_kb(file_path) >= size_threshold_kb

def collect_files_to_compress(directory: Path, size_threshold_kb: float) -> List[Path]:
    return [
        f for f in directory.rglob("*")
        if f.is_file() and should_compress(f, size_threshold_kb)
    ]

def compress_file(file_path: Path, output_dir: Path) -> Tuple[Path, float, float]:
    zip_name = output_dir / f"{file_path.stem}.zip"
    with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(file_path, arcname=file_path.name)
    original_size = get_file_size_kb(file_path)
    zip_size = get_file_size_kb(zip_name)
    return zip_name, original_size, zip_size
