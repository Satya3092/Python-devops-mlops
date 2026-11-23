# Day 062 — Practice Tasks: Logging Module

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: First logger

**Problem statement:** Configure logging at WARNING level (format `LEVEL: message`, to stdout) and emit one message of each level. Only 3 should appear.

**Input requirements:** No user input required.

**Expected behavior:** WARNING, ERROR, CRITICAL lines.

**Expected output:**

```text
WARNING: warning
ERROR: error
CRITICAL: critical
```

## Task 2 — Medium: Log to a file

**Problem statement:** Configure a logger named `deploy` that writes INFO+ to `deploy.log` with format `%(levelname)s %(message)s`. Log 3 deployment steps and one error, then print the file.

**Input requirements:** No user input required.

**Expected behavior:** Four lines from the log file.

**Expected output:**

```text
INFO Pulling image orders:2.4.1
INFO Applying manifests
INFO Waiting for rollout
ERROR Rollout timed out
```

## Task 3 — Practical Challenge: Instrument a function

**Problem statement:** Write `process_orders(orders, logger)` that logs DEBUG for each order, WARNING for orders with amount > 1000, and uses `logger.exception` for orders with a missing amount (KeyError), continuing with the rest. Log a final INFO summary. Use a console handler with format `%(levelname)s %(message)s` at DEBUG level.

**Input requirements:** No user input required.

**Expected behavior:** Debug lines, a warning, an exception message with traceback, and a summary.

**Expected output:**

```text
DEBUG Processing order 1 (250.00)
DEBUG Processing order 2 (4999.99)
WARNING Large order 2: 4999.99
ERROR Order 3 has no amount
Traceback (most recent call last):
  File "solutions/solution.py", in process_orders
    amount = order["amount"]
             ~~~~~^^^^^^^^^^
KeyError: 'amount'
INFO Processed 2 of 3 orders
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
