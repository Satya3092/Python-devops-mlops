# Day 048 — Practice Tasks: Writing Files

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Multiplication file

**Problem statement:** Write the multiplication table of 9 (1–10) to `table9.txt`, then print the file.

**Input requirements:** No user input required.

**Expected behavior:** Ten lines `9 x n = ...`.

**Expected output:**

```text
9 x 1 = 9
9 x 2 = 18
9 x 3 = 27
9 x 4 = 36
9 x 5 = 45
9 x 6 = 54
9 x 7 = 63
9 x 8 = 72
9 x 9 = 81
9 x 10 = 90
```

## Task 2 — Medium: Do not overwrite

**Problem statement:** Use mode `"x"` to create `release_notes.txt`. Try to create it a second time and catch the `FileExistsError`, printing a friendly message.

**Input requirements:** No user input required.

**Expected behavior:** First creation succeeds, second prints `release_notes.txt already exists`.

**Expected output:**

```text
Created release_notes.txt
release_notes.txt already exists
```

## Task 3 — Practical Challenge: Generate an nginx upstream config

**Problem statement:** Given backends `[("10.0.1.10", 8080), ("10.0.1.11", 8080), ("10.0.1.12", 8081)]`, generate `upstream.conf` containing an `upstream app_backend { ... }` block with one `server ip:port;` line each, plus `keepalive 32;`. Print the generated file.

**Input requirements:** No user input required.

**Expected behavior:** A valid-looking nginx upstream block.

**Expected output:**

```text
upstream app_backend {
    server 10.0.1.10:8080;
    server 10.0.1.11:8080;
    server 10.0.1.12:8081;
    keepalive 32;
}
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
