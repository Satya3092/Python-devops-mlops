# Day 060 — Shutil Module

[⬅ Day 059](../../06-modules-oop/day-059/README.md) | [📚 Phase 6: Advanced Python and OOP](../README.md) | [🏠 Home](../../README.md) | [Day 061 ➡](../../06-modules-oop/day-061/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 6 — Advanced Python and OOP | 🟡 Intermediate | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Copy, move and delete files and directory trees
- Create and extract archives (`zip`, `tar.gz`)
- Check disk usage and find executables with `shutil`

## 2. Topic Explanation

`shutil` ("shell utilities") provides **high-level** file operations — the Python versions of `cp`, `mv`, `rm -rf`, `tar` and `df`.

| Task | shutil |
|---|---|
| `cp file dest` | `shutil.copy(src, dst)` |
| `cp -p file dest` (keep metadata) | `shutil.copy2(src, dst)` |
| `cp -r dir dest` | `shutil.copytree(src, dst)` |
| `mv src dst` | `shutil.move(src, dst)` |
| `rm -rf dir` | `shutil.rmtree(dir)` ⚠️ |
| `tar czf name.tar.gz dir` | `shutil.make_archive("name", "gztar", "dir")` |
| `tar xzf archive` | `shutil.unpack_archive("archive.tar.gz", "dest")` |
| `df -h /` | `shutil.disk_usage("/")` |
| `which docker` | `shutil.which("docker")` |

⚠️ `rmtree` deletes everything with no recycle bin. In real automation, add a **dry-run** mode and double-check paths before deleting.

`copytree(..., ignore=shutil.ignore_patterns("*.pyc", "__pycache__"))` skips unwanted files.

## 3. Syntax

```python
import shutil
shutil.copy2("src.txt", "dst.txt")
shutil.copytree("src_dir", "dst_dir", dirs_exist_ok=True)
shutil.move("a", "b")
shutil.rmtree("dir")
shutil.make_archive("backup", "gztar", root_dir="folder")
total, used, free = shutil.disk_usage("/")
```

| Part | Meaning |
|---|---|
| `copy / copy2` | Copy a file (copy2 also keeps timestamps). |
| `copytree` | Recursive copy of a folder. |
| `rmtree` | Recursive delete — dangerous. |
| `make_archive / unpack_archive` | Create/extract zip, tar, gztar... |
| `disk_usage / which` | Disk space and executable lookup. |

## 4. Example 1 — Basic Example: Copy, move, archive

```python
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
```

## 5. Example 2 — Practical Example: Backup with rotation and a disk-space guard

```python
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
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `copy2` keeps timestamps — important for backups.
- `copytree` with `ignore_patterns` skips compiled and backup files (like a `.dockerignore`).
- `make_archive("release-v1.0", "gztar", root_dir=...)` creates `release-v1.0.tar.gz` and returns its path.
- `unpack_archive` detects the format automatically.

**Example 2**
- `disk_usage` returns bytes; we refuse to run if free space is too low (`raise SystemExit` stops the script with a message).
- Three dated backups are created, then all but the newest `KEEP` are deleted — a classic retention policy.
- `shutil.which` checks that required tools exist before a script relies on them.

## 7. Expected Output

**Example 1:**

```text
Backup created: True
Copied tree: ['app_release_copy/app.py', 'app_release_copy/config', 'app_release_copy/config/settings.yaml']
Archive created: release-v1.0.tar.gz
Extracted files: ['app.py', 'settings.yaml']
Copy removed: True
```

**Example 2:**

```text
Disk space check passed
Created website-2026-11-18.tar.gz
Created website-2026-11-19.tar.gz
Created website-2026-11-20.tar.gz
Rotated out website-2026-11-18.tar.gz
Kept: ['website-2026-11-19.tar.gz', 'website-2026-11-20.tar.gz']
python3                found
tar                    found
definitely-not-a-tool  NOT found
```

> ℹ️ Your values (paths, hostnames, sizes, times) will differ from the output shown — it depends on your machine. Examples that call Linux commands work on Linux, macOS and WSL.

## 8. Common Mistakes

**1. `rmtree` on the wrong path**

A variable that is empty or `/` can wipe data. Validate paths and support a dry-run mode.

**2. `copytree` into an existing folder**

Raises `FileExistsError` unless you pass `dirs_exist_ok=True` (Python 3.8+).

**3. `make_archive` extension confusion**

Pass the base name *without* extension; shutil adds `.tar.gz`/`.zip` itself.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Copy a config:** Create `nginx.conf` with one line, copy it to `nginx.conf.bak` with `copy2`, and print both file sizes.
- **Task 2 (Medium) — Zip a folder:** Create a folder `report_files/` with 3 text files, archive it as `reports.zip`, extract it to `restored/`, and print the restored file names.
- **Task 3 (Practical Challenge) — Disk report:** Write `disk_report(path=".")` that returns a dict with total, used and free in GB (2 decimals) plus `used_percent`, and prints `WARNING` if used_percent > 80. Then check for required tools `["git", "tar", "terraform"]` with `shutil.which` and print a pre-flight summary.

## 10. DevOps/MLOps Connection

- **DevOps:** backups with retention, packaging build artefacts, cleaning workspaces in CI, pre-flight checks (`which kubectl`).
- **Cloud:** zip a Lambda deployment package with `make_archive` before uploading it.
- **MLOps:** archive a model with its config and metrics as one versioned artefact.

## 11. Interview Questions

**Q1. What is the difference between `shutil.copy` and `shutil.copy2`?**

<details><summary>Show answer</summary>

`copy2` also preserves metadata such as modification time.

</details>

**Q2. How do you delete a non-empty directory in Python?**

<details><summary>Show answer</summary>

`shutil.rmtree(path)` — carefully, ideally with validation and dry-run support.

</details>

**Q3. How do you check free disk space in Python?**

<details><summary>Show answer</summary>

`shutil.disk_usage(path)` returns total, used and free bytes (or `psutil.disk_usage`).

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 60 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 059](../../06-modules-oop/day-059/README.md) | [📚 Phase 6: Advanced Python and OOP](../README.md) | [🏠 Home](../../README.md) | [Day 061 ➡](../../06-modules-oop/day-061/README.md)
