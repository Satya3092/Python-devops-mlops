"""
Day 070 — Automating Files and Directories: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
import os
import time
from pathlib import Path

NOW = time.time()
DAY = 86400

# ===== Task 1 =====
folder = Path("newest_demo")
folder.mkdir(exist_ok=True)
for name, age in [("a.txt", 1), ("b.txt", 5), ("c.txt", 2), ("d.txt", 10)]:
    p = folder / name
    p.write_text(name)
    os.utime(p, (NOW - age * DAY, NOW - age * DAY))
files = sorted(folder.iterdir(), key=lambda p: p.stat().st_mtime)
print("Newest:", files[-1].name)
print("Oldest:", files[0].name)

# ===== Task 2 =====
tree = Path("ext_demo")
for name, size in [("a.log", 3000), ("logs/b.log", 5000), ("data/c.csv", 12000), ("d.json", 800), ("data/e.csv", 4000)]:
    p = tree / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("x" * size)
totals = {}
for p in tree.rglob("*"):
    if p.is_file():
        totals[p.suffix] = totals.get(p.suffix, 0) + p.stat().st_size
for ext, size in sorted(totals.items(), key=lambda kv: kv[1], reverse=True):
    print(f"{ext:<6}{size:>7} bytes")

# ===== Task 3 =====
def apply_retention(folder, keep_daily=3, dry_run=True):
    backups = sorted(Path(folder).glob("backup-*.tar.gz"))
    newest = set(backups[-keep_daily:])
    for b in backups:
        date = b.name[len("backup-"):-len(".tar.gz")]
        if b in newest or date.endswith("-01"):
            print("keep  ", b.name)
        else:
            print("delete" if not dry_run else "would delete", b.name)
            if not dry_run:
                b.unlink()


bdir = Path("retention_demo")
bdir.mkdir(exist_ok=True)
for d in ["2026-10-25", "2026-10-26", "2026-10-27", "2026-10-28", "2026-10-29", "2026-10-30",
          "2026-10-31", "2026-11-01", "2026-11-02", "2026-11-03"]:
    (bdir / f"backup-{d}.tar.gz").write_text("data")
apply_retention(bdir, dry_run=False)
print("Left:", len(list(bdir.iterdir())), "backups")
