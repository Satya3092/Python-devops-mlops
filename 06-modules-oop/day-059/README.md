# Day 059 — Pathlib Module

[⬅ Day 058](../../06-modules-oop/day-058/README.md) | [📚 Phase 6: Advanced Python and OOP](../README.md) | [🏠 Home](../../README.md) | [Day 060 ➡](../../06-modules-oop/day-060/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 6 — Advanced Python and OOP | 🟡 Intermediate | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Represent paths as `Path` objects
- Build paths with `/`, read parts like `.name`, `.suffix`, `.parent`
- Find files with `glob`/`rglob` and read/write files in one line

## 2. Topic Explanation

`pathlib` (Python 3.4+) treats paths as **objects** instead of strings. It is the modern, recommended way to work with the filesystem.

```python
from pathlib import Path
log_dir = Path("/var/log")
nginx_log = log_dir / "nginx" / "access.log"   # join with /
```

Useful attributes and methods:

| Code | Result for `Path("/data/backup.tar.gz")` |
|---|---|
| `.name` | `backup.tar.gz` |
| `.stem` | `backup.tar` |
| `.suffix` / `.suffixes` | `.gz` / `['.tar', '.gz']` |
| `.parent` | `/data` |
| `.exists()`, `.is_file()`, `.is_dir()` | checks |
| `.mkdir(parents=True, exist_ok=True)` | `mkdir -p` |
| `.glob("*.log")`, `.rglob("*.py")` | find files (recursive with `rglob`) |
| `.read_text()`, `.write_text()` | read/write a whole text file |
| `.stat().st_size`, `.stat().st_mtime` | size, modification time |
| `Path.home()`, `Path.cwd()` | home and current directory |
| `Path(__file__).resolve().parent` | folder of the running script |

The last one is extremely useful: it lets a script find files **next to itself**, no matter where it is run from.

## 3. Syntax

```python
from pathlib import Path
p = Path("folder") / "file.txt"
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text("hello", encoding="utf-8")
text = p.read_text(encoding="utf-8")
for f in Path(".").rglob("*.log"): ...
```

| Part | Meaning |
|---|---|
| `Path(...)` | Creates a path object. |
| `/` | Joins path segments. |
| `.name / .stem / .suffix / .parent` | Parts of the path. |
| `.glob() / .rglob()` | Pattern search (rglob = recursive). |
| `.read_text() / .write_text()` | Whole-file read/write. |

## 4. Example 1 — Basic Example: Path objects and their parts

```python
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
```

## 5. Example 2 — Practical Example: Organise a downloads folder by file type

```python
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
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- Parts of a path are attributes — no string slicing needed.
- `.suffixes` handles double extensions like `.tar.gz`.
- `Path("etc") / "myapp" / "config.yaml"` joins safely on every OS.
- `Path(__file__).resolve().parent` is the folder of the current script.

**Example 2**
- `write_text` creates sample files in one line.
- `glob("*")` lists the folder; each file is classified by `.suffix`.
- `next((... for ...), "other")` returns the first matching category or `"other"`.
- `shutil.move` (Day 60) moves the file into its category folder.
- `rglob("*.csv")` searches recursively; `.stat().st_size` gives sizes.

## 7. Expected Output

**Example 1:**

```text
name: backup-2026-11-20.tar.gz
stem: backup-2026-11-20.tar
suffix: .gz
suffixes: ['.tar', '.gz']
parent: /data/backups/postgres
parts: ('/', 'data', 'backups', 'postgres', 'backup-2026-11-20.tar.gz')
with new name: /data/backups/postgres/latest.tar.gz
joined: etc/myapp/config.yaml
as posix string: etc/myapp/config.yaml
This script lives in a folder called: day-059
```

**Example 2:**

```text
data       ['data.csv', 'sales.csv']
documents  ['notes.txt', 'report.pdf']
images     ['diagram.png', 'photo.jpg']
other      ['setup.sh']
All CSV files (recursive): ['data.csv', 'sales.csv']
Total bytes: 148
```

> ℹ️ The folder-name line shows the folder where you saved the script.

## 8. Common Mistakes

**1. Mixing strings and Paths carelessly**

`"folder" / "file"` fails (two strings). At least one side must be a `Path`.

**2. Expecting `.suffix` to return `.tar.gz`**

It returns only the last suffix `.gz`. Use `.suffixes` or `name.endswith(".tar.gz")`.

**3. Paths relative to the working directory**

Scripts run from cron or CI often have a different working dir. Use `Path(__file__).resolve().parent / "data.csv"`.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Path anatomy:** For `Path("/home/ubuntu/projects/api/main.py")` print name, stem, suffix, parent and the grandparent (`parents[1]`).
- **Task 2 (Medium) — Find Python files:** Create `code_demo/` with nested folders containing 3 `.py` files and 2 `.md` files. Use `rglob` to print every `.py` file path relative to `code_demo`, sorted.
- **Task 3 (Practical Challenge) — Keep the newest backups:** Create a folder `backups_demo` with 6 files `db-2026-11-15.sql.gz` … `db-2026-11-20.sql.gz`. Using pathlib, keep the newest 3 (by the date in the name) and delete the rest. Print what was deleted and what remains.

## 10. DevOps/MLOps Connection

- **DevOps:** cleaner file automation (backup retention, artefact collection, config discovery) that works on Linux and Windows runners.
- **Cloud:** walking a build folder with `rglob` to upload artefacts to S3.
- **MLOps:** `Path(__file__).parent / "models" / "model.joblib"` lets a FastAPI app find its model regardless of where it is started (Day 98).

## 11. Interview Questions

**Q1. Why prefer pathlib over os.path?**

<details><summary>Show answer</summary>

It is object-oriented, more readable (`/` joining), cross-platform, and groups path operations as methods.

</details>

**Q2. How do you find all `.log` files recursively?**

<details><summary>Show answer</summary>

`Path(root).rglob("*.log")`.

</details>

**Q3. How do you get the directory of the current script?**

<details><summary>Show answer</summary>

`Path(__file__).resolve().parent`.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 59 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 058](../../06-modules-oop/day-058/README.md) | [📚 Phase 6: Advanced Python and OOP](../README.md) | [🏠 Home](../../README.md) | [Day 060 ➡](../../06-modules-oop/day-060/README.md)
