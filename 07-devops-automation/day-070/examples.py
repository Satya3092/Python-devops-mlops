"""
Day 070 — Automating Files and Directories
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Finding old and large files
# ======================================================================
import os
import time
from pathlib import Path

NOW = time.time()
DAY = 86400

base = Path("var_log_demo")
samples = {"app.log": (0, 1_200), "app.log.1": (3, 50_000), "app.log.2": (9, 52_000),
           "nginx/access.log": (1, 300_000), "nginx/access.log.5": (35, 900_000), "notes.txt": (60, 100)}
for name, (age_days, size) in samples.items():
    path = base / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("x" * size)
    timestamp = NOW - age_days * DAY
    os.utime(path, (timestamp, timestamp))        # fake the modification time


def find_files(base, pattern="*", older_than_days=0, min_size=0):
    for path in sorted(Path(base).rglob(pattern)):
        if not path.is_file():
            continue
        stat = path.stat()
        age = (NOW - stat.st_mtime) / DAY
        if age >= older_than_days and stat.st_size >= min_size:
            yield path, round(age), stat.st_size      # 'yield' = return items one by one


print("Logs older than 7 days:")
for path, age, size in find_files(base, "*.log*", older_than_days=7):
    print(f"  {path.as_posix():<34} {age:>3} days {size / 1024:>7.1f} KB")

print("Files bigger than 100 KB:")
for path, age, size in find_files(base, min_size=100_000):
    print(f"  {path.as_posix():<34} {size / 1024:>7.1f} KB")

# ======================================================================
# Example 2 — A safe cleanup job: archive, delete, dedupe
# ======================================================================
import hashlib
import os
import shutil
import time
from pathlib import Path

NOW = time.time()
DAY = 86400
base = Path("cleanup_demo")
for name, age, content in [("logs/app-1.log", 20, "old log A"), ("logs/app-2.log", 15, "old log B"),
                           ("logs/app-3.log", 1, "fresh log"), ("tmp/build-cache.tmp", 2, "cache"),
                           ("uploads/photo.jpg", 5, "same image bytes"), ("uploads/photo-copy.jpg", 4, "same image bytes")]:
    path = base / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    os.utime(path, (NOW - age * DAY, NOW - age * DAY))


def cleanup(base, retention_days=14, dry_run=True):
    base = Path(base).resolve()
    actions = []
    old_logs = [p for p in base.glob("logs/*.log") if (NOW - p.stat().st_mtime) / DAY > retention_days]
    if old_logs:
        archive_dir = base / "archive"
        if not dry_run:
            archive_dir.mkdir(exist_ok=True)
            staging = archive_dir / "staging"
            staging.mkdir(exist_ok=True)
            for p in old_logs:
                shutil.move(str(p), str(staging / p.name))
            shutil.make_archive(str(archive_dir / "old-logs"), "gztar", root_dir=staging)
            shutil.rmtree(staging)
        actions.append(f"archive {len(old_logs)} old logs -> archive/old-logs.tar.gz")
    for tmp in base.rglob("*.tmp"):
        if not dry_run:
            tmp.unlink()
        actions.append(f"delete {tmp.relative_to(base).as_posix()}")
    seen = {}
    for path in sorted(base.glob("uploads/*")):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest in seen:
            actions.append(f"duplicate {path.name} == {seen[digest].name} (sha256 {digest[:12]}...)")
        else:
            seen[digest] = path
    return actions


print("=== DRY RUN ===")
for action in cleanup(base):
    print("  would", action)
print("=== REAL RUN ===")
for action in cleanup(base, dry_run=False):
    print("  did", action)
print("Remaining files:", sorted(p.relative_to(base).as_posix() for p in base.rglob("*") if p.is_file()))
