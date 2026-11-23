# Day 070 — Automating Files and Directories

[⬅ Day 069](../../07-devops-automation/day-069/README.md) | [📚 Phase 7: Python for DevOps Automation](../README.md) | [🏠 Home](../../README.md) | [Day 071 ➡](../../07-devops-automation/day-071/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 7 — Python for DevOps Automation | 🟠 Intermediate+ | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Find files by age, size and pattern
- Build safe cleanup and archiving jobs with dry-run support
- Detect duplicate files with checksums (`hashlib`)

## 2. Topic Explanation

Disks fill up with old logs, temp files, build artefacts and forgotten backups. File automation keeps servers healthy.

Building blocks:
- `Path.rglob(pattern)` — find files.
- `path.stat().st_mtime` — last modification time (seconds since 1970). Compare with `time.time()` to get the age.
- `path.stat().st_size` — size in bytes.
- `shutil.move`, `shutil.make_archive`, `path.unlink()` — act on files.
- `hashlib.sha256(data).hexdigest()` — a **checksum**: identical content ⇒ identical hash. Used to find duplicates and verify downloads/artefacts.

Safety rules for destructive jobs:
1. **Dry-run by default** — print what *would* happen.
2. **Restrict the scope** — only inside a known base directory, only matching patterns.
3. **Log every action.**
4. **Archive before deleting** when data might be needed.

This is the Python version of `find /var/log -name "*.log" -mtime +7 -delete` — but testable, portable and with reporting.

## 3. Syntax

```python
import time, hashlib
from pathlib import Path
age_days = (time.time() - path.stat().st_mtime) / 86400
for path in Path(base).rglob("*.log"):
    if age_days > 7: ...
digest = hashlib.sha256(path.read_bytes()).hexdigest()
```

| Part | Meaning |
|---|---|
| `st_mtime` | Last modification time as a Unix timestamp. |
| `time.time()` | Current Unix timestamp. |
| `86400` | Seconds per day. |
| `hashlib.sha256()` | Cryptographic checksum of bytes. |
| `dry_run` | Report actions without performing them. |

## 4. Example 1 — Basic Example: Finding old and large files

```python
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
```

## 5. Example 2 — Practical Example: A safe cleanup job: archive, delete, dedupe

```python
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
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `os.utime` sets fake modification times so the demo is reproducible.
- `find_files` is a **generator** (it uses `yield`): it produces matching files one by one, which is memory-friendly for huge trees.
- Age is `(now - mtime) / 86400`; size comes from `stat().st_size`.

**Example 2**
- `cleanup` is **dry-run by default** — the first run only reports.
- Old logs are moved into a staging folder, compressed into one archive, then the staging folder is removed.
- Temporary files are deleted.
- Duplicates are detected by comparing SHA-256 checksums of file contents (file names don't matter). We only *report* duplicates — deleting user uploads automatically is risky.

## 7. Expected Output

**Example 1:**

```text
Logs older than 7 days:
  var_log_demo/app.log.2               9 days    50.8 KB
  var_log_demo/nginx/access.log.5     35 days   878.9 KB
Files bigger than 100 KB:
  var_log_demo/nginx/access.log        293.0 KB
  var_log_demo/nginx/access.log.5      878.9 KB
```

**Example 2:**

```text
=== DRY RUN ===
  would archive 2 old logs -> archive/old-logs.tar.gz
  would delete tmp/build-cache.tmp
  would duplicate photo.jpg == photo-copy.jpg (sha256 f10266197016...)
=== REAL RUN ===
  did archive 2 old logs -> archive/old-logs.tar.gz
  did delete tmp/build-cache.tmp
  did duplicate photo.jpg == photo-copy.jpg (sha256 f10266197016...)
Remaining files: ['archive/old-logs.tar.gz', 'logs/app-3.log', 'uploads/photo-copy.jpg', 'uploads/photo.jpg']
```

## 8. Common Mistakes

**1. Deleting without a dry run**

Always test destructive scripts in dry-run mode and review the output first.

**2. Unbounded paths**

A bug that sets `base` to `/` could wipe a server. Validate that paths are inside an allowed directory (`path.resolve().is_relative_to(base)`).

**3. Comparing duplicates by name or size only**

Different files can share names/sizes. Compare checksums.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Newest file:** Create 4 files in `newest_demo/` with modification times 1, 5, 2 and 10 days ago, then print the newest and the oldest file names.
- **Task 2 (Medium) — Size by extension:** Create a small tree with `.log`, `.csv` and `.json` files of different sizes and print the total size per extension (sorted largest first) using `rglob` and `stat`.
- **Task 3 (Practical Challenge) — Retention policy:** Write `apply_retention(folder, keep_daily=3)` for files named `backup-YYYY-MM-DD.tar.gz`: keep the newest N backups plus any backup from the 1st of a month (monthly backups), delete the rest. Support `dry_run`. Test with 10 daily backups from 2026-10-25 to 2026-11-03.

## 10. DevOps/MLOps Connection

- **DevOps:** log/artefact cleanup, backup retention, finding disk hogs, verifying artefact checksums in pipelines.
- **Cloud:** S3 lifecycle rules implement the same ideas (transition to Glacier, expire after N days) — your script is the on-prem equivalent.
- **MLOps:** keep the last N model checkpoints plus the best one; deduplicate datasets by hash; checksums detect when training data changed (data versioning tools like DVC use hashes).

## 11. Interview Questions

**Q1. How do you find files older than N days in Python?**

<details><summary>Show answer</summary>

Compare `time.time() - path.stat().st_mtime` with `N * 86400` while iterating with `rglob` or `os.walk`.

</details>

**Q2. Why compute checksums of files?**

<details><summary>Show answer</summary>

To detect duplicates, verify integrity after transfer, and detect changes (caching, data versioning).

</details>

**Q3. How do you make a destructive script safer?**

<details><summary>Show answer</summary>

Dry-run default, limited scope, explicit confirmation flags, logging, backups/archives before deletion, and tests.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 70 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 069](../../07-devops-automation/day-069/README.md) | [📚 Phase 7: Python for DevOps Automation](../README.md) | [🏠 Home](../../README.md) | [Day 071 ➡](../../07-devops-automation/day-071/README.md)
