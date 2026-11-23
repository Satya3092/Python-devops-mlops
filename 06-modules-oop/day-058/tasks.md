# Day 058 — Practice Tasks: OS Module

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Create a project skeleton

**Problem statement:** Create folders `myapp/src`, `myapp/tests`, `myapp/docs` and an empty `myapp/README.md`, then print the sorted contents of `myapp`.

**Input requirements:** No user input required.

**Expected behavior:** `['README.md', 'docs', 'src', 'tests']`.

**Expected output:**

```text
['README.md', 'docs', 'src', 'tests']
```

## Task 2 — Medium: Extension counter

**Problem statement:** Create 6 files with mixed extensions in a folder `mixed/`, then count files per extension with `os.listdir` and `os.path.splitext`.

**Input requirements:** No user input required.

**Expected behavior:** A dict like `{'.log': 3, '.csv': 2, '.txt': 1}`.

**Expected output:**

```text
{'.log': 3, '.csv': 2, '.txt': 1}
```

## Task 3 — Practical Challenge: Disk usage report (du-like)

**Problem statement:** Build a tree `storage/` with subfolders `images` (3 files), `backups` (2 big files) and `tmp` (4 small files). Using `os.walk`, print the total size of each top-level subfolder in KB, sorted largest first, and the percentage of the total.

**Input requirements:** No user input required.

**Expected behavior:** backups largest with the highest percentage.

**Expected output:**

```text
backups    1220.7 KB   90.6%
images      122.1 KB    9.1%
tmp           4.9 KB    0.4%
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
