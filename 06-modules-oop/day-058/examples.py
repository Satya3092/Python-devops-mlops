"""
Day 058 — OS Module
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Working with directories and files
# ======================================================================
import os

print("Current dir name:", os.path.basename(os.getcwd()))

os.makedirs("sandbox/logs/archive", exist_ok=True)
for name in ("app.log", "error.log", "notes.txt"):
    with open(os.path.join("sandbox", "logs", name), "w") as f:
        f.write("sample\n")

print("Contents of sandbox/logs:", sorted(os.listdir("sandbox/logs")))

old = os.path.join("sandbox", "logs", "error.log")
new = os.path.join("sandbox", "logs", "archive", "error-2026-11-20.log")
os.rename(old, new)
print("Moved error.log ->", os.path.relpath(new, "sandbox"))

path = os.path.join("sandbox", "logs", "app.log")
print("exists:", os.path.exists(path), "| is file:", os.path.isfile(path),
      "| is dir:", os.path.isdir("sandbox/logs"))
print("splitext:", os.path.splitext("backup.tar.gz"))

os.remove(os.path.join("sandbox", "logs", "notes.txt"))
print("After remove:", sorted(os.listdir("sandbox/logs")))

# ======================================================================
# Example 2 — Walking a tree: find large and old-style files
# ======================================================================
import os

# Build a small fake project tree
layout = {
    "project/src/app.py": 1200,
    "project/src/utils.py": 300,
    "project/data/train.csv": 250_000,
    "project/data/raw/dump.sql": 1_500_000,
    "project/logs/app.log": 80_000,
    "project/logs/app.log.1": 95_000,
}
for path, size in layout.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write("x" * size)

total_size = 0
by_extension = {}
large_files = []
for folder, subfolders, files in os.walk("project"):
    subfolders.sort()                               # deterministic order
    for name in sorted(files):
        full_path = os.path.join(folder, name)
        size = os.path.getsize(full_path)
        total_size += size
        ext = os.path.splitext(name)[1] or "(none)"
        by_extension[ext] = by_extension.get(ext, 0) + size
        if size > 100_000:
            large_files.append((full_path, size))

print(f"Total size: {total_size / 1024:.1f} KB")
print("Size by extension:")
for ext, size in sorted(by_extension.items(), key=lambda kv: kv[1], reverse=True):
    print(f"  {ext:<7} {size / 1024:>8.1f} KB")
print("Files > 100 KB:")
for path, size in large_files:
    print(f"  {path} ({size / 1024:.0f} KB)")

print("HOME is set:", "HOME" in os.environ or "USERPROFILE" in os.environ)
print("APP_ENV =", os.environ.get("APP_ENV", "not set (default: dev)"))
