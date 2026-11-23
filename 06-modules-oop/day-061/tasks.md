# Day 061 — Practice Tasks: Subprocess Module

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Python version

**Problem statement:** Run `python --version` via `sys.executable` and print only the version number.

**Input requirements:** No user input required.

**Expected behavior:** Prints something like `3.12.4`.

**Expected output:**

```text
3.13.18
```

## Task 2 — Medium: Git information

**Problem statement:** Write `git_info()` that returns a dict with git's version (or `not installed`) using `shutil.which` and `subprocess.run`. Print it.

**Input requirements:** No user input required.

**Expected behavior:** A dict with the git version.

**Expected output:**

```text
{'git': '2.43.0'}
```

## Task 3 — Practical Challenge: Service status checker

**Problem statement:** Write `count_lines(command)` that runs a command and returns how many lines it printed, and `top_processes(n)` that runs `ps -eo pid,comm,%mem --sort=-%mem` and returns the top n as a list of tuples `(pid, name, mem_percent)`. Print the top 3 processes in a table. Handle errors gracefully.

**Input requirements:** No user input required.

**Expected behavior:** A table of 3 processes (values differ per machine).

**Expected output:**

```text
Lines printed by 'ps -e': True
    PID  NAME              %MEM
   1342  dockerd            3.1
    987  containerd         1.8
   2210  python3            0.9
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
