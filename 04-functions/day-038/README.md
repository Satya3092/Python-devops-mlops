# Day 038 — Return Statement

[⬅ Day 037](../../04-functions/day-037/README.md) | [📚 Phase 4: Functions and Modular Programming](../README.md) | [🏠 Home](../../README.md) | [Day 039 ➡](../../04-functions/day-039/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 4 — Functions and Modular Programming | 🟡 Beginner+ | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Send results back from a function with `return`
- Return multiple values (tuples)
- Understand `None` and early returns

## 2. Topic Explanation

`print()` shows a value on screen. `return` **hands a value back to the caller** so it can be stored, tested or passed to another function.

```python
def square(n):
    return n * n

result = square(4)        # result is 16
print(square(3) + 1)      # 10
```

Key points:
- `return` immediately **ends** the function.
- A function without `return` returns `None`.
- `return a, b` returns a **tuple** — unpack it with `x, y = func()`.
- **Early return** (guard clause): exit as soon as you know the answer; it avoids deep nesting.

Analogy: `print` is a chef shouting "the soup is ready!". `return` is the chef handing you the bowl so you can actually eat it.

This is the most important habit for testable code: **functions should return values; the caller decides whether to print them.**

## 3. Syntax

```python
def function_name(params):
    ...
    return value

result = function_name(args)
a, b = function_returning_two_values()
```

| Part | Meaning |
|---|---|
| `return value` | Ends the function and gives `value` to the caller. |
| `return a, b` | Returns a tuple `(a, b)`. |
| `return (no value)` | Ends the function and returns `None`. |
| `result = f()` | Captures the returned value. |

## 4. Example 1 — Basic Example: print vs return

```python
def add_print(a, b):
    print(a + b)            # shows the value but returns None


def add_return(a, b):
    return a + b            # gives the value back


x = add_print(2, 3)
y = add_return(2, 3)
print("x is", x)
print("y is", y)
print("y * 10 =", y * 10)


def min_max(numbers):
    return min(numbers), max(numbers)


low, high = min_max([7, 2, 9, 4])
print("Low:", low, "High:", high)
```

## 5. Example 2 — Practical Example: Composable health-check functions

```python
def percent(used, total):
    """Return usage as a percentage, or 0.0 when total is zero."""
    if total == 0:
        return 0.0                      # early return (guard clause)
    return used / total * 100


def classify(value, warning=75, critical=90):
    """Return OK / WARNING / CRITICAL for a percentage."""
    if value >= critical:
        return "CRITICAL"
    if value >= warning:
        return "WARNING"
    return "OK"


def check_server(name, mem_used, mem_total, disk_used, disk_total):
    """Return a dict with the results so other code can use them."""
    mem_pct = percent(mem_used, mem_total)
    disk_pct = percent(disk_used, disk_total)
    return {
        "name": name,
        "memory": (round(mem_pct, 1), classify(mem_pct)),
        "disk": (round(disk_pct, 1), classify(disk_pct)),
    }


results = [
    check_server("web-01", 6.2, 8, 40, 100),
    check_server("db-01", 30, 32, 410, 500),
    check_server("new-vm", 0, 0, 1, 50),
]
for r in results:
    print(f"{r['name']:<7} memory={r['memory']} disk={r['disk']}")

critical_servers = [r["name"] for r in results if "CRITICAL" in (r["memory"][1], r["disk"][1])]
print("Critical servers:", critical_servers)
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `add_print` prints 5 but returns `None`, so `x` is `None`.
- `add_return` returns 5, so `y` can be used in further calculations.
- `min_max` returns a tuple which is unpacked into `low` and `high`.

**Example 2**
- `percent` uses a guard clause: if `total` is 0 it returns immediately, avoiding a ZeroDivisionError.
- `classify` returns as soon as a condition matches — no `elif` chain needed.
- `check_server` **composes** the two smaller functions and returns a dict.
- Because results are returned (not printed), we can filter them afterwards to find critical servers.

## 7. Expected Output

**Example 1:**

```text
5
x is None
y is 5
y * 10 = 50
Low: 2 High: 9
```

**Example 2:**

```text
web-01  memory=(77.5, 'WARNING') disk=(40.0, 'OK')
db-01   memory=(93.8, 'CRITICAL') disk=(82.0, 'WARNING')
new-vm  memory=(0.0, 'OK') disk=(2.0, 'OK')
Critical servers: ['db-01']
```

## 8. Common Mistakes

**1. Printing instead of returning**

A function that only prints cannot be reused in calculations or tests. Return the value; print it outside.

**2. Code after `return`**

Lines after `return` in the same block never run (dead code).

**3. Forgetting to return in one branch**

If only some branches have `return`, other paths return `None`, causing `TypeError` later.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Celsius to Fahrenheit:** Write `to_fahrenheit(celsius)` that returns the converted value. Print the result for 0, 37 and 100.
- **Task 2 (Medium) — Validate a port:** Write `is_valid_port(port)` that returns `True` if the port is an int between 1 and 65535. Test with 22, 0, 70000 and 8080.
- **Task 3 (Practical Challenge) — Parse a log line:** Write `parse_log_line(line)` that returns a tuple `(date, time, level, message)` for lines like `2026-11-20 10:15:32 ERROR Database timeout`, or `None` if the line has fewer than 4 parts. Use it on a list of lines and count levels with the returned values.

## 10. DevOps/MLOps Connection

- **DevOps:** functions that return structured results (dicts/tuples) can feed reports, alerts, JSON output and unit tests.
- **Cloud:** Lambda handlers `return` a response dict to API Gateway.
- **MLOps:** `evaluate(model, X, y)` returns metrics that decide whether a model is promoted; `predict()` returns predictions to an API.

## 11. Interview Questions

**Q1. What does a function return if it has no `return` statement?**

<details><summary>Show answer</summary>

`None`.

</details>

**Q2. How can a function return multiple values?**

<details><summary>Show answer</summary>

By returning a tuple (`return a, b`), list or dict; the caller unpacks it.

</details>

**Q3. What is a guard clause?**

<details><summary>Show answer</summary>

An early `return` at the start of a function for special/invalid cases, which keeps the main logic un-nested.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 38 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 037](../../04-functions/day-037/README.md) | [📚 Phase 4: Functions and Modular Programming](../README.md) | [🏠 Home](../../README.md) | [Day 039 ➡](../../04-functions/day-039/README.md)
