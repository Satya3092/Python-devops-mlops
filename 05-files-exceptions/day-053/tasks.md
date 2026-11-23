# Day 053 — Practice Tasks: try, except, else, finally

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Trace the flow

**Problem statement:** Write `check(value)` that converts value to int inside try, prints `invalid` in except, `valid: n` in else and `checked` in finally. Call it with `"7"` and `"x"`.

**Input requirements:** No user input required.

**Expected behavior:** valid: 7 / checked / invalid / checked.

**Expected output:**

```text
valid: 7
checked
invalid
checked
```

## Task 2 — Medium: Always close the connection

**Problem statement:** Simulate a database connection with a dict `{"open": True}`. Write `run_query(conn, query)` that raises `ValueError` for queries containing `DROP`, and always sets `conn["open"] = False` in `finally`. Show the connection is closed after a good and a bad query.

**Input requirements:** No user input required.

**Expected behavior:** Both runs end with `open: False`.

**Expected output:**

```text
Executed: SELECT * FROM orders
open: False
Error: dangerous query blocked
open: False
```

## Task 3 — Practical Challenge: Retry with finally-based metrics

**Problem statement:** Write `fetch_with_retry(results, max_attempts=3)` where `results` is a list of booleans simulating each attempt. Use try/except/else/finally inside a loop: raise `ConnectionError` on False, return on success in `else`, and count attempts in `finally`. Re-raise the last error if all attempts fail. Test success on attempt 2, and total failure.

**Input requirements:** No user input required.

**Expected behavior:** Success after 2 attempts; failure re-raised after 3 and caught by the caller.

**Expected output:**

```text
retrying: attempt 1 failed
success after 2 attempts
retrying: attempt 1 failed
retrying: attempt 2 failed
retrying: attempt 3 failed
Gave up: attempt 3 failed
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
