# Day 046 — File Handling Introduction

[⬅ Day 045](../../04-functions/day-045/README.md) | [📚 Phase 5: File Handling and Error Handling](../README.md) | [🏠 Home](../../README.md) | [Day 047 ➡](../../05-files-exceptions/day-047/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 5 — File Handling and Error Handling | 🟡 Intermediate | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Understand files, paths and file modes
- Open and close files safely with the `with` statement
- Check if a file exists before using it

## 2. Topic Explanation

Variables live in memory and vanish when the program ends. **Files** store data permanently on disk — logs, configs, reports, datasets, trained models.

Working with a file has three steps: **open → read/write → close**.

```python
with open("welcome.txt", "r") as file:
    content = file.read()
```

- `open(path, mode)` returns a **file object**.
- `with` (a *context manager*) **closes the file automatically**, even if an error happens. Always use it.
- **Paths:** `"welcome.txt"` is *relative* to the folder you run the program from; `"/var/log/syslog"` is *absolute*.

| Mode | Meaning |
|---|---|
| `"r"` | read (default) — error if missing |
| `"w"` | write — **creates or empties** the file |
| `"a"` | append — add to the end |
| `"x"` | create — error if it exists |
| `"b"` | binary, combine e.g. `"rb"` for images/models |

Always pass `encoding="utf-8"` for text files so behaviour is identical on Windows and Linux.

Analogy: `with open(...)` is like borrowing a library book with an automatic return — no matter what happens, the book goes back.

> Run the examples from inside this day's folder (`cd` into it first) so the relative file paths work.

## 3. Syntax

```python
with open("path/to/file.txt", "r", encoding="utf-8") as file:
    data = file.read()
# file is closed here

import os
os.path.exists("file.txt")
```

| Part | Meaning |
|---|---|
| `open(path, mode)` | Opens a file and returns a file object. |
| `with ... as file:` | Context manager — closes the file automatically. |
| `encoding="utf-8"` | Text encoding; use it for all text files. |
| `os.path.exists()` | True if the path exists. |

## 4. Example 1 — Basic Example: Reading a file with `with`

```python
import os

filename = "welcome.txt"
print("Exists?", os.path.exists(filename))

with open(filename, "r", encoding="utf-8") as file:
    content = file.read()
    print("Inside with - closed?", file.closed)

print("Outside with - closed?", file.closed)
print("Content:")
print(content)
print("Characters:", len(content))
```

## 5. Example 2 — Practical Example: Writing a small status file and reading it back

```python
import os

status_file = "deploy_status.txt"

with open(status_file, "w", encoding="utf-8") as file:
    file.write("service=orders-api\n")
    file.write("version=2.4.1\n")
    file.write("status=success\n")

print("File size:", os.path.getsize(status_file), "bytes")

with open(status_file, "r", encoding="utf-8") as file:
    for line in file:
        key, value = line.strip().split("=")
        print(f"{key:<8}: {value}")

if os.path.exists("missing.txt"):
    print("missing.txt found")
else:
    print("missing.txt does not exist - skipping")
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `os.path.exists` checks the file before opening it.
- Inside the `with` block the file is open; after the block `file.closed` is `True` — Python closed it for us.

**Example 2**
- Mode `"w"` creates `deploy_status.txt` (or empties it if it exists). `write()` does not add newlines, so we add `\n`.
- `os.path.getsize` returns the size in bytes.
- Looping over a file object yields one line at a time; `strip()` removes the newline.
- Checking existence first avoids a crash for optional files.

## 7. Expected Output

**Example 1:**

```text
Exists? True
Inside with - closed? False
Outside with - closed? True
Content:
Welcome to file handling!
Files let programs remember data after they stop running.

Characters: 84
```

**Example 2:**

```text
File size: 48 bytes
service : orders-api
version : 2.4.1
status  : success
missing.txt does not exist - skipping
```

## 8. Common Mistakes

**1. Forgetting to close files**

Without `with`, an exception can leave files open (and data unwritten). Always use `with open(...)`.

**2. Using `"w"` by accident**

Opening an existing file with `"w"` **erases it immediately**. Use `"a"` to add or `"x"` to refuse overwriting.

**3. Relative path confusion**

`FileNotFoundError` often means you ran the script from a different folder. Print `os.getcwd()` to see where you are.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Hello file:** Write `Hello from Python!` to `hello.txt`, then read and print it.
- **Task 2 (Medium) — Safe open:** Ask whether `config.ini` exists using `os.path.exists`. If not, create it with two lines `[app]` and `debug=false`; then print its contents and its size in bytes.
- **Task 3 (Practical Challenge) — Server list file:** Write a list of 5 hostnames to `servers.txt` (one per line). Then read the file back, count the lines, and print each hostname with a line number.

## 10. DevOps/MLOps Connection

- **DevOps:** reading configs, writing reports and state files, rotating logs, generating inventory files for Ansible.
- **Cloud:** files are uploaded to/downloaded from S3; Lambda can write to `/tmp`.
- **Data engineering:** every pipeline reads raw files and writes processed files.
- **MLOps:** datasets are loaded from files and trained models are saved to files (Day 97).

## 11. Interview Questions

**Q1. Why use `with open(...)`?**

<details><summary>Show answer</summary>

It guarantees the file is closed (and buffers flushed) even if an exception occurs.

</details>

**Q2. What is the difference between modes `w` and `a`?**

<details><summary>Show answer</summary>

`w` truncates (empties) the file before writing; `a` appends to the end.

</details>

**Q3. What is the difference between a relative and an absolute path?**

<details><summary>Show answer</summary>

An absolute path starts at the filesystem root; a relative path is resolved from the current working directory.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 46 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 045](../../04-functions/day-045/README.md) | [📚 Phase 5: File Handling and Error Handling](../README.md) | [🏠 Home](../../README.md) | [Day 047 ➡](../../05-files-exceptions/day-047/README.md)
