# Day 031 — Range Function

[⬅ Day 030](../../03-dictionaries-logic/day-030/README.md) | [📚 Phase 3: Dictionaries and Programming Logic](../README.md) | [🏠 Home](../../README.md) | [Day 032 ➡](../../03-dictionaries-logic/day-032/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 3 — Dictionaries and Programming Logic | 🟢 Beginner | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Generate number sequences with `range(stop)`, `range(start, stop)`, `range(start, stop, step)`
- Count backwards with negative steps
- Use `range` to drive loops and build lists

## 2. Topic Explanation

`range()` produces a sequence of integers — perfect for "do this N times" or numbering things.

| Call | Numbers |
|---|---|
| `range(5)` | 0, 1, 2, 3, 4 |
| `range(1, 6)` | 1, 2, 3, 4, 5 |
| `range(0, 20, 5)` | 0, 5, 10, 15 |
| `range(10, 0, -2)` | 10, 8, 6, 4, 2 |

Like slicing, the **stop value is excluded**.

`range` is **lazy**: it does not create all numbers in memory, it generates them on demand. `range(1_000_000_000)` costs almost no memory. Use `list(range(...))` when you need an actual list.

Bash equivalent: `for i in $(seq 1 5)` or `{1..5}`.

## 3. Syntax

```python
range(stop)
range(start, stop)
range(start, stop, step)
```

| Part | Meaning |
|---|---|
| `start` | First number (default 0). |
| `stop` | Sequence ends BEFORE this number. |
| `step` | Increment (default 1); negative counts down. |
| `list(range(...))` | Materialise the numbers into a list. |

## 4. Example 1 — Basic Example: range variations

```python
print(list(range(5)))
print(list(range(1, 6)))
print(list(range(0, 20, 5)))
print(list(range(10, 0, -2)))
print("Length of range(1, 100):", len(range(1, 100)))

for i in range(3):
    print("Hello number", i)

total = 0
for n in range(1, 101):
    total += n
print("Sum 1..100 =", total)
```

## 5. Example 2 — Practical Example: Generating names, IPs and port ranges

```python
# Generate 5 worker hostnames: worker-01 ... worker-05
hostnames = [f"worker-{n:02d}" for n in range(1, 6)]
print(hostnames)

# Assign IP addresses from 10.0.1.10 upwards
for offset, host in enumerate(hostnames):
    print(f"{host} -> 10.0.1.{10 + offset}")

# Every 15 minutes in an hour (cron-like schedule)
print("Backup minutes:", list(range(0, 60, 15)))

# Port range for NodePort services (sample of the first five)
node_ports = range(30000, 32768)
print("Number of NodePorts available:", len(node_ports))
print("First five:", list(node_ports[:5]))

# Countdown before a maintenance window
for minutes_left in range(15, 0, -5):
    print(f"Maintenance starts in {minutes_left} minutes")
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `range(10, 0, -2)` counts down; it stops before 0.
- `len(range(1, 100))` is 99 — the stop value is excluded.
- Summing with a loop over `range(1, 101)` gives 5050.

**Example 2**
- `f"worker-{n:02d}"` pads numbers to two digits.
- `range(0, 60, 15)` gives cron-like minute marks.
- A `range` object supports `len()` and even slicing without creating a full list.

## 7. Expected Output

**Example 1:**

```text
[0, 1, 2, 3, 4]
[1, 2, 3, 4, 5]
[0, 5, 10, 15]
[10, 8, 6, 4, 2]
Length of range(1, 100): 99
Hello number 0
Hello number 1
Hello number 2
Sum 1..100 = 5050
```

**Example 2:**

```text
['worker-01', 'worker-02', 'worker-03', 'worker-04', 'worker-05']
worker-01 -> 10.0.1.10
worker-02 -> 10.0.1.11
worker-03 -> 10.0.1.12
worker-04 -> 10.0.1.13
worker-05 -> 10.0.1.14
Backup minutes: [0, 15, 30, 45]
Number of NodePorts available: 2768
First five: [30000, 30001, 30002, 30003, 30004]
Maintenance starts in 15 minutes
Maintenance starts in 10 minutes
Maintenance starts in 5 minutes
```

## 8. Common Mistakes

**1. Expecting the stop value**

`range(1, 10)` ends at 9. Use `range(1, 11)` to include 10.

**2. Using `range(len(lst))` unnecessarily**

`for i in range(len(items)): items[i]` is un-Pythonic. Loop directly or use `enumerate`.

**3. Float steps**

`range(0, 1, 0.1)` → `TypeError`. `range` works only with integers.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Even numbers:** Print all even numbers from 2 to 20 using a step.
- **Task 2 (Medium) — Subnet hosts:** Generate the list of IP addresses `192.168.1.1` to `192.168.1.10` and print them on one line separated by commas.
- **Task 3 (Practical Challenge) — Cron schedule preview:** A job runs every 7 minutes starting at minute 3 within an hour. Print all minute marks, how many runs per hour, and the runs in a full day (24 hours). Then print the first 5 run times in HH:MM format starting from 00:03.

## 10. DevOps/MLOps Connection

- **DevOps:** creating numbered resources (`web-01`..`web-10`), retry counters, IP or port ranges.
- **Cloud:** Terraform's `count` and Python's `range` express the same idea: N similar resources.
- **ML:** `for epoch in range(num_epochs):` is the heart of every training loop.

## 11. Interview Questions

**Q1. Does `range(1, 5)` include 5?**

<details><summary>Show answer</summary>

No. It yields 1, 2, 3, 4.

</details>

**Q2. Why is `range` memory efficient?**

<details><summary>Show answer</summary>

It is a lazy sequence object that computes values on demand instead of storing them all.

</details>

**Q3. How do you count down from 10 to 1?**

<details><summary>Show answer</summary>

`range(10, 0, -1)`.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 31 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 030](../../03-dictionaries-logic/day-030/README.md) | [📚 Phase 3: Dictionaries and Programming Logic](../README.md) | [🏠 Home](../../README.md) | [Day 032 ➡](../../03-dictionaries-logic/day-032/README.md)
