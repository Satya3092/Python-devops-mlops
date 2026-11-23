# Day 004 — Practice Tasks: Python Literals

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Readable numbers

**Problem statement:** Store the number of requests per day `86400000` using underscores, the max file size 0xFFFF and permission 0o644. Print each value in decimal.

**Input requirements:** No user input required.

**Expected behavior:** Prints 86400000, 65535 and 420.

**Expected output:**

```text
Requests/day: 86400000
Max file size: 65535
Permission 0o644 in decimal: 420
```

## Task 2 — Medium: Formatted report with escapes

**Problem statement:** Print a small table using `\t` between columns and `\n` between rows for services nginx (80), postgres (5432) and redis (6379) — using a single `print()` call.

**Input requirements:** No user input required.

**Expected behavior:** Three aligned rows below a header.

**Expected output:**

```text
SERVICE	PORT
nginx	80
postgres	5432
redis	6379
```

## Task 3 — Practical Challenge: Generate a Dockerfile

**Problem statement:** Use a triple-quoted string to create the text of a simple Dockerfile (FROM python:3.12-slim, WORKDIR /app, COPY, RUN pip install, CMD). Print it, then print how many lines it has using `.count("\n") + 1`.

**Input requirements:** No user input required.

**Expected behavior:** Prints the Dockerfile followed by `Lines: 5`.

**Expected output:**

```text
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
Lines: 5
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
