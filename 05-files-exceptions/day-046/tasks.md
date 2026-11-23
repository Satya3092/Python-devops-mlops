# Day 046 — Practice Tasks: File Handling Introduction

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Hello file

**Problem statement:** Write `Hello from Python!` to `hello.txt`, then read and print it.

**Input requirements:** No user input required.

**Expected behavior:** Prints the text that was written.

**Expected output:**

```text
Hello from Python!
```

## Task 2 — Medium: Safe open

**Problem statement:** Ask whether `config.ini` exists using `os.path.exists`. If not, create it with two lines `[app]` and `debug=false`; then print its contents and its size in bytes.

**Input requirements:** No user input required.

**Expected behavior:** Creates the file and prints its contents and size.

**Expected output:**

```text
[app]
debug=false
Size: 18 bytes
```

## Task 3 — Practical Challenge: Server list file

**Problem statement:** Write a list of 5 hostnames to `servers.txt` (one per line). Then read the file back, count the lines, and print each hostname with a line number.

**Input requirements:** No user input required.

**Expected behavior:** Five numbered hostnames and `Total: 5`.

**Expected output:**

```text
1 web-01
2 web-02
3 web-03
4 db-01
5 cache-01
Total: 5
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
