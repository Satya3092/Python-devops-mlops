"""
Day 059 — Pathlib Module
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Path objects and their parts
# ======================================================================
from pathlib import Path

p = Path("/data/backups/postgres/backup-2026-11-20.tar.gz")
print("name:", p.name)
print("stem:", p.stem)
print("suffix:", p.suffix)
print("suffixes:", p.suffixes)
print("parent:", p.parent)
print("parts:", p.parts)
print("with new name:", p.with_name("latest.tar.gz"))

config = Path("etc") / "myapp" / "config.yaml"
print("joined:", config)
print("as posix string:", config.as_posix())

script_folder = Path(__file__).resolve().parent
print("This script lives in a folder called:", script_folder.name)

# ======================================================================
# Example 2 — Organise a downloads folder by file type
# ======================================================================
from pathlib import Path
import shutil

downloads = Path("downloads_demo")
downloads.mkdir(exist_ok=True)
for name in ["report.pdf", "photo.jpg", "data.csv", "notes.txt", "diagram.png", "sales.csv", "setup.sh"]:
    (downloads / name).write_text(f"content of {name}\n", encoding="utf-8")

CATEGORIES = {
    "documents": {".pdf", ".txt"},
    "images": {".jpg", ".png"},
    "data": {".csv"},
}

moved = {}
for file in sorted(downloads.glob("*")):
    if not file.is_file():
        continue
    category = next((c for c, exts in CATEGORIES.items() if file.suffix in exts), "other")
    target_dir = downloads / category
    target_dir.mkdir(exist_ok=True)
    shutil.move(str(file), str(target_dir / file.name))
    moved.setdefault(category, []).append(file.name)

for category, names in sorted(moved.items()):
    print(f"{category:<10} {names}")

print("All CSV files (recursive):", sorted(p.name for p in downloads.rglob("*.csv")))
total = sum(p.stat().st_size for p in downloads.rglob("*") if p.is_file())
print("Total bytes:", total)
