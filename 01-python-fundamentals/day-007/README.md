# Day 007 — Arithmetic Operators

[⬅ Day 006](../../01-python-fundamentals/day-006/README.md) | [📚 Phase 1: Python Fundamentals](../README.md) | [🏠 Home](../../README.md) | [Day 008 ➡](../../01-python-fundamentals/day-008/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 1 — Python Fundamentals | 🟢 Beginner | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Use `+ - * / // % **` correctly
- Know the difference between `/` and `//`
- Use `%` (modulo) to find remainders and `divmod()`

## 2. Topic Explanation

Arithmetic operators do maths.

| Operator | Name | Example | Result |
|---|---|---|---|
| `+` | Addition | `7 + 2` | `9` |
| `-` | Subtraction | `7 - 2` | `5` |
| `*` | Multiplication | `7 * 2` | `14` |
| `/` | Division (always float) | `7 / 2` | `3.5` |
| `//` | Floor division (whole part) | `7 // 2` | `3` |
| `%` | Modulo (remainder) | `7 % 2` | `1` |
| `**` | Power | `2 ** 10` | `1024` |

Analogy for `//` and `%`: you have 7 pods and nodes that hold 2 pods each. `7 // 2 = 3` full nodes, `7 % 2 = 1` pod left over.

`divmod(a, b)` returns both at once: `(a // b, a % b)`.

`+` and `*` also work on strings: `"ab" + "cd"` joins, `"-" * 5` repeats.

## 3. Syntax

```python
result = a + b    a - b    a * b    a / b
result = a // b   a % b    a ** b
quotient, remainder = divmod(a, b)
```

| Part | Meaning |
|---|---|
| `/` | True division — the result is always a `float`. |
| `//` | Floor division — rounds down to the nearest whole number. |
| `%` | Modulo — the remainder after division. |
| `**` | Exponent (power). |
| `divmod(a, b)` | Returns a pair `(a // b, a % b)`. |

## 4. Example 1 — Basic Example: All arithmetic operators

```python
a = 17
b = 5
print("a + b  =", a + b)
print("a - b  =", a - b)
print("a * b  =", a * b)
print("a / b  =", a / b)
print("a // b =", a // b)
print("a % b  =", a % b)
print("a ** 2 =", a ** 2)
print("divmod(a, b) =", divmod(a, b))
```

## 5. Example 2 — Practical Example: Capacity planning and uptime

```python
# How many nodes do we need for 23 pods if each node fits 4 pods?
total_pods = 23
pods_per_node = 4
full_nodes = total_pods // pods_per_node
leftover_pods = total_pods % pods_per_node
nodes_needed = full_nodes + (1 if leftover_pods > 0 else 0)
print("Full nodes:", full_nodes, "| leftover pods:", leftover_pods)
print("Nodes needed:", nodes_needed)

# Convert uptime in seconds to days, hours, minutes
uptime_seconds = 400_000
days, remainder = divmod(uptime_seconds, 86_400)
hours, remainder = divmod(remainder, 3_600)
minutes = remainder // 60
print("Uptime:", days, "days", hours, "hours", minutes, "minutes")

# Storage growth: 50 GB growing 10% per month for 12 months
storage_gb = 50 * 1.10 ** 12
print("Storage after 12 months:", round(storage_gb, 1), "GB")
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1** shows each operator with `a = 17`, `b = 5`. Note `17 / 5` is `3.4` (float) while `17 // 5` is `3`.

**Example 2**
- `total_pods // pods_per_node` gives 5 full nodes; `%` shows 3 pods remain, so we need a 6th node.
- `(1 if leftover_pods > 0 else 0)` is a one-line condition (you will study conditions on Day 12).
- `divmod(uptime_seconds, 86_400)` splits seconds into whole days and the remaining seconds; repeated for hours.
- `1.10 ** 12` is compound growth: 10% per month for 12 months.

## 7. Expected Output

**Example 1:**

```text
a + b  = 22
a - b  = 12
a * b  = 85
a / b  = 3.4
a // b = 3
a % b  = 2
a ** 2 = 289
divmod(a, b) = (3, 2)
```

**Example 2:**

```text
Full nodes: 5 | leftover pods: 3
Nodes needed: 6
Uptime: 4 days 15 hours 6 minutes
Storage after 12 months: 156.9 GB
```

## 8. Common Mistakes

**1. Expecting `/` to return an int**

`10 / 2` is `5.0`, a float. Use `//` when you need a whole number.

**2. Using `^` for power**

`2 ^ 3` is bitwise XOR (= 1), not 8. Use `2 ** 3`.

**3. Division by zero**

`x / 0` raises `ZeroDivisionError`. Check the divisor first (or handle the error, Day 52).

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Even or odd number of replicas:** Given `replicas = 7`, print the remainder of dividing by 2 and explain if the number is even (remainder 0) or odd.
- **Task 2 (Medium) — Seconds formatter:** Convert `backup_duration = 9876` seconds into hours, minutes and seconds using `//` and `%` (or divmod).
- **Task 3 (Practical Challenge) — Monthly AWS cost estimate:** An EC2 instance costs $0.0416/hour, an EBS volume 100 GB at $0.08 per GB-month, and data transfer 250 GB at $0.09/GB. Calculate the monthly cost (730 hours), the yearly cost, and how many whole instances fit into a $200 monthly budget.

## 10. DevOps/MLOps Connection

- **DevOps / Kubernetes:** capacity planning (`pods // per_node`), sharding with `%` (e.g. `host_id % 3` decides which of 3 backup windows a server uses).
- **Cloud:** cost estimation scripts are pure arithmetic over pricing data.
- **Monitoring:** converting bytes → GB (`/ 1024 ** 3`) and seconds → readable uptime.
- **ML:** loss functions, normalisation and metrics are arithmetic on numbers (vectorised with NumPy on Day 85).

## 11. Interview Questions

**Q1. What is the difference between `/` and `//`?**

<details><summary>Show answer</summary>

`/` is true division and returns a float. `//` is floor division and rounds down to an integer value (float if an operand is float).

</details>

**Q2. What is `-7 // 2` in Python?**

<details><summary>Show answer</summary>

`-4`, because floor division rounds toward negative infinity.

</details>

**Q3. Give a practical use of the modulo operator.**

<details><summary>Show answer</summary>

Checking even/odd, round-robin distribution (`index % num_servers`), running a task every Nth iteration, or converting seconds into minutes/seconds.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 7 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 006](../../01-python-fundamentals/day-006/README.md) | [📚 Phase 1: Python Fundamentals](../README.md) | [🏠 Home](../../README.md) | [Day 008 ➡](../../01-python-fundamentals/day-008/README.md)
