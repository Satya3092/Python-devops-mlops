# Day 070 — Practice Tasks: Automating Files and Directories

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Newest file

**Problem statement:** Create 4 files in `newest_demo/` with modification times 1, 5, 2 and 10 days ago, then print the newest and the oldest file names.

**Input requirements:** No user input required.

**Expected behavior:** Newest: the 1-day file; oldest: the 10-day file.

**Expected output:**

```text
Newest: a.txt
Oldest: d.txt
```

## Task 2 — Medium: Size by extension

**Problem statement:** Create a small tree with `.log`, `.csv` and `.json` files of different sizes and print the total size per extension (sorted largest first) using `rglob` and `stat`.

**Input requirements:** No user input required.

**Expected behavior:** A sorted size report.

**Expected output:**

```text
.csv    16000 bytes
.log     8000 bytes
.json     800 bytes
```

## Task 3 — Practical Challenge: Retention policy

**Problem statement:** Write `apply_retention(folder, keep_daily=3)` for files named `backup-YYYY-MM-DD.tar.gz`: keep the newest N backups plus any backup from the 1st of a month (monthly backups), delete the rest. Support `dry_run`. Test with 10 daily backups from 2026-10-25 to 2026-11-03.

**Input requirements:** No user input required.

**Expected behavior:** Keeps 3 newest + 2026-11-01; deletes 6.

**Expected output:**

```text
delete backup-2026-10-25.tar.gz
delete backup-2026-10-26.tar.gz
delete backup-2026-10-27.tar.gz
delete backup-2026-10-28.tar.gz
delete backup-2026-10-29.tar.gz
delete backup-2026-10-30.tar.gz
delete backup-2026-10-31.tar.gz
keep   backup-2026-11-01.tar.gz
keep   backup-2026-11-02.tar.gz
keep   backup-2026-11-03.tar.gz
Left: 3 backups
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
