"""
Day 058 — OS Module: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
import os

# ===== Task 1 =====
for sub in ("src", "tests", "docs"):
    os.makedirs(os.path.join("myapp", sub), exist_ok=True)
open(os.path.join("myapp", "README.md"), "w").close()
print(sorted(os.listdir("myapp")))

# ===== Task 2 =====
os.makedirs("mixed", exist_ok=True)
for name in ["a.log", "b.log", "c.log", "data1.csv", "data2.csv", "notes.txt"]:
    open(os.path.join("mixed", name), "w").close()
counts = {}
for name in os.listdir("mixed"):
    ext = os.path.splitext(name)[1]
    counts[ext] = counts.get(ext, 0) + 1
print(dict(sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))))

# ===== Task 3 =====
spec = {"images": [40_000, 55_000, 30_000], "backups": [500_000, 750_000], "tmp": [1_000, 2_000, 500, 1_500]}
for folder, sizes in spec.items():
    os.makedirs(os.path.join("storage", folder), exist_ok=True)
    for i, size in enumerate(sizes):
        with open(os.path.join("storage", folder, f"file{i}.bin"), "w") as f:
            f.write("x" * size)
usage = {}
for folder, _, files in os.walk("storage"):
    if folder == "storage":
        continue
    top = os.path.relpath(folder, "storage").split(os.sep)[0]
    usage[top] = usage.get(top, 0) + sum(os.path.getsize(os.path.join(folder, f)) for f in files)
total = sum(usage.values())
for name, size in sorted(usage.items(), key=lambda kv: kv[1], reverse=True):
    print(f"{name:<8} {size / 1024:>8.1f} KB  {size / total * 100:5.1f}%")
