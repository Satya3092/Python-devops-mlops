# Day 029 — For Loops

[⬅ Day 028](../../03-dictionaries-logic/day-028/README.md) | [📚 Phase 3: Dictionaries and Programming Logic](../README.md) | [🏠 Home](../../README.md) | [Day 030 ➡](../../03-dictionaries-logic/day-030/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 3 — Dictionaries and Programming Logic | 🟢 Beginner | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Repeat actions for every item in a collection with `for`
- Loop over strings, lists, tuples, dicts and sets
- Use `enumerate()` and `zip()`
- Use the loop-`else` clause

## 2. Topic Explanation

A **for loop** repeats a block of code once for **each item** in a collection (an *iterable*):

```python
for server in ["web-01", "web-02", "db-01"]:
    print("Pinging", server)
```

- `server` is the **loop variable**; it takes each value in turn.
- The indented block is the **loop body**.

Analogy: a for loop is a postal worker visiting every house on a street list — same action, different address each time.

Bash equivalent: `for s in web-01 web-02 db-01; do echo "Pinging $s"; done`

Helpers:
- `enumerate(items, start=1)` gives `(index, item)` pairs — no manual counter needed.
- `zip(a, b)` walks two lists side by side.
- `for k, v in d.items()` loops over a dict.
- A `for ... else` block runs `else` only if the loop was **not** stopped by `break` (Day 32).

## 3. Syntax

```python
for item in iterable:
    do_something(item)

for index, item in enumerate(items, start=1):
    ...
for a, b in zip(list_a, list_b):
    ...
```

| Part | Meaning |
|---|---|
| `for` | Starts the loop. |
| `item` | Loop variable — holds the current element. |
| `in iterable` | Any collection: list, string, dict, range, file... |
| `enumerate()` | Adds a counter. |
| `zip()` | Pairs items from several iterables. |

## 4. Example 1 — Basic Example: Looping over different collections

```python
for letter in "Py":
    print("Letter:", letter)

fruits = ["apple", "mango", "banana"]
for fruit in fruits:
    print("I like", fruit)

for number, fruit in enumerate(fruits, start=1):
    print(number, fruit)

prices = [40, 90, 15]
for fruit, price in zip(fruits, prices):
    print(f"{fruit} costs {price}")

stock = {"apple": 10, "mango": 0}
for item, quantity in stock.items():
    print(item, "in stock" if quantity > 0 else "SOLD OUT")
```

## 5. Example 2 — Practical Example: Checking a fleet of servers

```python
servers = [
    {"name": "web-01", "cpu": 45, "disk": 60, "status": "running"},
    {"name": "web-02", "cpu": 92, "disk": 71, "status": "running"},
    {"name": "db-01", "cpu": 30, "disk": 94, "status": "running"},
    {"name": "batch-01", "cpu": 0, "disk": 20, "status": "stopped"},
]

alerts = []
total_cpu = 0
running = 0

for number, server in enumerate(servers, start=1):
    print(f"[{number}/{len(servers)}] Checking {server['name']}...")
    if server["status"] != "running":
        print("    skipped (not running)")
        continue                       # skip to the next server (Day 32)
    running += 1
    total_cpu += server["cpu"]
    if server["cpu"] > 90:
        alerts.append(f"{server['name']}: CPU {server['cpu']}%")
    if server["disk"] > 90:
        alerts.append(f"{server['name']}: disk {server['disk']}%")

print(f"Average CPU of running servers: {total_cpu / running:.1f}%")
print("Alerts:")
for alert in alerts:
    print("  -", alert)
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- Looping over a string yields one character at a time.
- `enumerate(fruits, start=1)` returns `(1, 'apple')`, `(2, 'mango')`, ...
- `zip(fruits, prices)` pairs elements at the same position.
- `stock.items()` provides key/value pairs.

**Example 2**
- Each iteration processes one server dict. `enumerate` gives a progress counter.
- `continue` skips the rest of the body for stopped servers.
- Running totals (`total_cpu += ...`) and an `alerts` list are built during the loop and reported afterwards.

## 7. Expected Output

**Example 1:**

```text
Letter: P
Letter: y
I like apple
I like mango
I like banana
1 apple
2 mango
3 banana
apple costs 40
mango costs 90
banana costs 15
apple in stock
mango SOLD OUT
```

**Example 2:**

```text
[1/4] Checking web-01...
[2/4] Checking web-02...
[3/4] Checking db-01...
[4/4] Checking batch-01...
    skipped (not running)
Average CPU of running servers: 55.7%
Alerts:
  - web-02: CPU 92%
  - db-01: disk 94%
```

## 8. Common Mistakes

**1. Forgetting the colon or indentation**

`for x in items` without `:` is a `SyntaxError`; un-indented body lines are outside the loop.

**2. Manual counters**

`i = 0 ... i += 1` is error-prone. Use `enumerate()`.

**3. Modifying a list while iterating**

Removing items from the list you loop over skips elements. Build a new list instead.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Multiplication table:** Print the multiplication table of 7 from 7 × 1 to 7 × 10.
- **Task 2 (Medium) — Service URLs:** Given `services = ["auth", "orders", "search"]` and `ports = [8001, 8002, 8003]`, print `http://<service>.internal:<port>/health` for each with a number prefix using `enumerate` and `zip`.
- **Task 3 (Practical Challenge) — Disk cleanup candidates:** Given files as tuples `(name, size_mb, days_old)`: `[("app.log", 120, 2), ("app.log.1", 300, 10), ("backup.tar", 4096, 40), ("core.dump", 2048, 15), ("notes.txt", 1, 100)]`, find files older than 7 days and bigger than 100 MB. Print each candidate and the total space you would free in GB.

## 10. DevOps/MLOps Connection

- **DevOps:** loop over servers to run commands, over files to rotate logs, over pods to check status.
- **Cloud:** iterate through every EC2 instance, S3 object or IAM user returned by boto3.
- **Data engineering:** process records one by one (or in batches) in ETL jobs.
- **ML:** training loops iterate over epochs and batches; evaluation loops over test samples.

## 11. Interview Questions

**Q1. What is an iterable?**

<details><summary>Show answer</summary>

Any object you can loop over with `for` — lists, tuples, strings, dicts, sets, files, generators, ranges.

</details>

**Q2. How do you get both index and value while looping?**

<details><summary>Show answer</summary>

`for i, value in enumerate(items):`.

</details>

**Q3. When does the `else` block of a for loop run?**

<details><summary>Show answer</summary>

When the loop finishes normally, i.e. without hitting `break`.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 29 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 028](../../03-dictionaries-logic/day-028/README.md) | [📚 Phase 3: Dictionaries and Programming Logic](../README.md) | [🏠 Home](../../README.md) | [Day 030 ➡](../../03-dictionaries-logic/day-030/README.md)
