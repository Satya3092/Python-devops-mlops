# Day 071 — Practice Tasks: Automating Linux Commands with subprocess

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Word frequency via pipeline

**Problem statement:** Pass the text `"apple banana apple cherry banana apple"` (one word per line) to `sort` then `uniq -c` then `sort -rn` using `input=` chaining, and print the result.

**Input requirements:** No user input required.

**Expected behavior:** apple 3, banana 2, cherry 1.

**Expected output:**

```text
apple 3
banana 2
cherry 1
```

## Task 2 — Medium: Live progress

**Problem statement:** Use `Popen` to run a child Python process that prints `Downloading part N` for N = 1..4, and prefix each received line with a timestamp-free counter `[k]` in the parent. Print the exit code.

**Input requirements:** No user input required.

**Expected behavior:** Four prefixed lines and exit code 0.

**Expected output:**

```text
[1] Downloading part 1
[2] Downloading part 2
[3] Downloading part 3
[4] Downloading part 4
exit code: 0
```

## Task 3 — Practical Challenge: Parallel command runner

**Problem statement:** Write `run_all(commands, workers=3)` that runs a dict of name → command list in parallel and returns name → (returncode, first line of output). Use it with 4 commands: `uname -s`, `python --version` (via sys.executable), `ls /nonexistent`, `echo done`. Print a summary table sorted by name and count failures.

**Input requirements:** No user input required.

**Expected behavior:** Four rows; one failure (`ls`).

**Expected output:**

```text
echo     rc=0   done
kernel   rc=0   Linux
missing  rc=2   ls
python   rc=0   Python 3.13.18
Failures: 1
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
