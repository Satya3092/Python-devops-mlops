# Day 060 — Practice Tasks: Shutil Module

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Copy a config

**Problem statement:** Create `nginx.conf` with one line, copy it to `nginx.conf.bak` with `copy2`, and print both file sizes.

**Input requirements:** No user input required.

**Expected behavior:** Two equal sizes.

**Expected output:**

```text
23 23
```

## Task 2 — Medium: Zip a folder

**Problem statement:** Create a folder `report_files/` with 3 text files, archive it as `reports.zip`, extract it to `restored/`, and print the restored file names.

**Input requirements:** No user input required.

**Expected behavior:** Three names.

**Expected output:**

```text
['report1.txt', 'report2.txt', 'report3.txt']
```

## Task 3 — Practical Challenge: Disk report

**Problem statement:** Write `disk_report(path=".")` that returns a dict with total, used and free in GB (2 decimals) plus `used_percent`, and prints `WARNING` if used_percent > 80. Then check for required tools `["git", "tar", "terraform"]` with `shutil.which` and print a pre-flight summary.

**Input requirements:** No user input required.

**Expected behavior:** Disk numbers and found/missing tools.

**Expected output:**

```text
{'total_gb': 49.09, 'used_gb': 38.12, 'free_gb': 10.97, 'used_percent': 77.7}
git        OK
tar        OK
terraform  MISSING
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
