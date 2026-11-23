# Day 038 — Practice Tasks: Return Statement

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Celsius to Fahrenheit

**Problem statement:** Write `to_fahrenheit(celsius)` that returns the converted value. Print the result for 0, 37 and 100.

**Input requirements:** No user input required.

**Expected behavior:** 32.0, 98.6, 212.0.

**Expected output:**

```text
0 C = 32.0 F
37 C = 98.6 F
100 C = 212.0 F
```

## Task 2 — Medium: Validate a port

**Problem statement:** Write `is_valid_port(port)` that returns `True` if the port is an int between 1 and 65535. Test with 22, 0, 70000 and 8080.

**Input requirements:** No user input required.

**Expected behavior:** True, False, False, True.

**Expected output:**

```text
22 True
0 False
70000 False
8080 True
```

## Task 3 — Practical Challenge: Parse a log line

**Problem statement:** Write `parse_log_line(line)` that returns a tuple `(date, time, level, message)` for lines like `2026-11-20 10:15:32 ERROR Database timeout`, or `None` if the line has fewer than 4 parts. Use it on a list of lines and count levels with the returned values.

**Input requirements:** No user input required.

**Expected behavior:** Parsed tuples, a skipped invalid line and the level counts.

**Expected output:**

```text
('2026-11-20', '10:15:32', 'ERROR', 'Database timeout')
('2026-11-20', '10:15:40', 'INFO', 'Retry succeeded')
Skipped invalid line: corrupted line
('2026-11-20', '10:16:02', 'ERROR', 'Disk full')
{'ERROR': 2, 'INFO': 1}
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
