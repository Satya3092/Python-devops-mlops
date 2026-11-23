# Day 058 — OS Module

[⬅ Day 057](../../06-modules-oop/day-057/README.md) | [📚 Phase 6: Advanced Python and OOP](../README.md) | [🏠 Home](../../README.md) | [Day 059 ➡](../../06-modules-oop/day-059/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 6 — Advanced Python and OOP | 🟡 Intermediate | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Inspect and change the current working directory
- List, create, rename and remove files and directories
- Read environment variables and system information with `os`

## 2. Topic Explanation

The `os` module is Python's interface to the **operating system** — the Python version of many shell commands.

| Shell | Python |
|---|---|
| `pwd` | `os.getcwd()` |
| `cd dir` | `os.chdir("dir")` |
| `ls` | `os.listdir(".")` |
| `mkdir -p a/b` | `os.makedirs("a/b", exist_ok=True)` |
| `mv a b` | `os.rename("a", "b")` |
| `rm file` | `os.remove("file")` |
| `rmdir dir` | `os.rmdir("dir")` (empty only) |
| `echo $HOME` | `os.environ.get("HOME")` |
| `find .` | `os.walk(".")` |

`os.path` contains path helpers: `join`, `exists`, `isfile`, `isdir`, `getsize`, `basename`, `dirname`, `splitext`, `abspath`.

`os.walk(top)` walks a directory tree and yields `(folder, subfolders, files)` for every folder — great for scanning projects or disks.

Tomorrow you will meet `pathlib`, a more modern, object-oriented alternative. You will see both styles in real projects.

## 3. Syntax

```python
import os
os.getcwd()                      os.listdir(path)
os.makedirs(path, exist_ok=True) os.rename(src, dst)
os.remove(file)                  os.rmdir(empty_dir)
os.environ.get("VAR", default)   os.path.join(a, b)
for folder, dirs, files in os.walk(top): ...
```

| Part | Meaning |
|---|---|
| `os.getcwd()` | Current working directory. |
| `os.makedirs(..., exist_ok=True)` | Create nested folders; no error if they exist. |
| `os.path.*` | Path inspection and manipulation helpers. |
| `os.walk()` | Recursive directory traversal. |
| `os.environ` | Dictionary-like access to environment variables. |

## 4. Example 1 — Basic Example: Working with directories and files

```python
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
```

## 5. Example 2 — Practical Example: Walking a tree: find large and old-style files

```python
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
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `os.makedirs(..., exist_ok=True)` behaves like `mkdir -p`.
- `os.path.join` builds paths with the correct separator.
- `os.rename` moves a file (here into an archive folder with a dated name — manual log rotation).
- `os.path.splitext` splits off only the **last** extension (`.gz`).

**Example 2**
- A fake tree is created, then `os.walk` visits every folder.
- Sorting `subfolders` in place makes the walk order deterministic.
- Sizes are aggregated per extension (like `du` grouped by type) and large files are flagged (like `find -size +100k`).
- `os.environ.get` reads environment variables with a default (Day 67 goes deeper).

## 7. Expected Output

**Example 1:**

```text
Current dir name: day-058
Contents of sandbox/logs: ['app.log', 'archive', 'error.log', 'notes.txt']
Moved error.log -> logs/archive/error-2026-11-20.log
exists: True | is file: True | is dir: True
splitext: ('backup.tar', '.gz')
After remove: ['app.log', 'archive']
```

**Example 2:**

```text
Total size: 1881.3 KB
Size by extension:
  .sql      1464.8 KB
  .csv       244.1 KB
  .1          92.8 KB
  .log        78.1 KB
  .py          1.5 KB
Files > 100 KB:
  project/data/train.csv (244 KB)
  project/data/raw/dump.sql (1465 KB)
HOME is set: True
APP_ENV = not set (default: dev)
```

## 8. Common Mistakes

**1. `os.rmdir` on non-empty folders**

It raises `OSError`. Use `shutil.rmtree` (Day 60) — carefully!

**2. `os.chdir` in scripts**

Changing directory affects the whole program and confuses relative paths. Prefer building absolute paths.

**3. String-concatenating paths**

`folder + "/" + name` breaks on Windows and doubles slashes. Use `os.path.join`.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Create a project skeleton:** Create folders `myapp/src`, `myapp/tests`, `myapp/docs` and an empty `myapp/README.md`, then print the sorted contents of `myapp`.
- **Task 2 (Medium) — Extension counter:** Create 6 files with mixed extensions in a folder `mixed/`, then count files per extension with `os.listdir` and `os.path.splitext`.
- **Task 3 (Practical Challenge) — Disk usage report (du-like):** Build a tree `storage/` with subfolders `images` (3 files), `backups` (2 big files) and `tmp` (4 small files). Using `os.walk`, print the total size of each top-level subfolder in KB, sorted largest first, and the percentage of the total.

## 10. DevOps/MLOps Connection

- **DevOps:** cleaning old files, rotating logs, scanning directories, preparing build folders, reading environment variables in containers.
- **Cloud:** walking a local directory to upload it to S3 (`aws s3 sync` in Python).
- **MLOps:** creating `models/`, `data/raw/`, `data/processed/` folders and finding the latest model file.

## 11. Interview Questions

**Q1. How do you create nested directories without an error if they exist?**

<details><summary>Show answer</summary>

`os.makedirs(path, exist_ok=True)`.

</details>

**Q2. What does `os.walk` return?**

<details><summary>Show answer</summary>

A generator of `(dirpath, dirnames, filenames)` tuples for each directory in the tree.

</details>

**Q3. How do you read an environment variable with a default?**

<details><summary>Show answer</summary>

`os.environ.get("NAME", "default")` or `os.getenv("NAME", "default")`.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 58 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 057](../../06-modules-oop/day-057/README.md) | [📚 Phase 6: Advanced Python and OOP](../README.md) | [🏠 Home](../../README.md) | [Day 059 ➡](../../06-modules-oop/day-059/README.md)
