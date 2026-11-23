"""
Day 060 — Shutil Module
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Copy, move, archive
# ======================================================================
import shutil
from pathlib import Path

app = Path("app_release")
(app / "config").mkdir(parents=True, exist_ok=True)
(app / "app.py").write_text("print('hello')\n")
(app / "config" / "settings.yaml").write_text("debug: false\n")
(app / "cache.pyc").write_text("binary junk")

shutil.copy2(app / "app.py", app / "app.py.bak")
print("Backup created:", (app / "app.py.bak").exists())

shutil.copytree(app, "app_release_copy", ignore=shutil.ignore_patterns("*.pyc", "*.bak"))
print("Copied tree:", sorted(p.as_posix() for p in Path("app_release_copy").rglob("*")))

archive = shutil.make_archive("release-v1.0", "gztar", root_dir="app_release_copy")
print("Archive created:", Path(archive).name)

shutil.unpack_archive(archive, "extracted")
print("Extracted files:", sorted(p.name for p in Path("extracted").rglob("*") if p.is_file()))

shutil.rmtree("app_release_copy")
print("Copy removed:", not Path("app_release_copy").exists())

# ======================================================================
# Example 2 — Backup with rotation and a disk-space guard
# ======================================================================
import shutil
from pathlib import Path

DATA_DIR = Path("website_data")
BACKUP_DIR = Path("website_backups")
KEEP = 2
MIN_FREE_GB = 1

# Sample data to back up
(DATA_DIR / "uploads").mkdir(parents=True, exist_ok=True)
(DATA_DIR / "index.html").write_text("<h1>Hello</h1>\n")
(DATA_DIR / "uploads" / "logo.png").write_text("fake image\n")
BACKUP_DIR.mkdir(exist_ok=True)

total, used, free = shutil.disk_usage(".")
free_gb = free / 1024 ** 3
if free_gb < MIN_FREE_GB:
    raise SystemExit(f"Not enough free space ({free_gb:.1f} GB)")
print("Disk space check passed")

for run in ["2026-11-18", "2026-11-19", "2026-11-20"]:
    base = BACKUP_DIR / f"website-{run}"
    created = shutil.make_archive(str(base), "gztar", root_dir=DATA_DIR)
    print("Created", Path(created).name)

backups = sorted(BACKUP_DIR.glob("website-*.tar.gz"))
for old in backups[:-KEEP]:
    old.unlink()
    print("Rotated out", old.name)
print("Kept:", [b.name for b in sorted(BACKUP_DIR.glob("*.tar.gz"))])

for tool in ["python3", "tar", "definitely-not-a-tool"]:
    location = shutil.which(tool)
    print(f"{tool:<22} {'found' if location else 'NOT found'}")
