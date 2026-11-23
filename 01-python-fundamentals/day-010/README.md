# Day 010 — Assignment Operators

[⬅ Day 009](../../01-python-fundamentals/day-009/README.md) | [📚 Phase 1: Python Fundamentals](../README.md) | [🏠 Home](../../README.md) | [Day 011 ➡](../../01-python-fundamentals/day-011/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 1 — Python Fundamentals | 🟢 Beginner | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Use compound assignment operators `+= -= *= /= //= %= **=`
- Build counters and running totals
- Understand that `x += 1` updates the variable in place of `x = x + 1`

## 2. Topic Explanation

Besides plain `=`, Python has **compound assignment operators** that update a variable using its current value.

| Operator | Same as |
|---|---|
| `x += 5` | `x = x + 5` |
| `x -= 5` | `x = x - 5` |
| `x *= 2` | `x = x * 2` |
| `x /= 2` | `x = x / 2` |
| `x //= 2` | `x = x // 2` |
| `x %= 3` | `x = x % 3` |
| `x **= 2` | `x = x ** 2` |

They are shorter and make intent clear: "increase the counter".

Analogy: a variable is a scoreboard. `score += 1` means "add one point to whatever the scoreboard currently shows".

`+=` also works on strings (append text) and lists (append items). Python has **no** `x++` operator.

## 3. Syntax

```python
variable += value
variable -= value
variable *= value      # and /=, //=, %=, **=
```

| Part | Meaning |
|---|---|
| `+=` | Add and store back. |
| `-=` | Subtract and store back. |
| `*=` | Multiply and store back. |
| `/= //= %= **=` | Divide, floor-divide, modulo, power — and store back. |

## 4. Example 1 — Basic Example: Updating a counter

```python
retries = 0
retries += 1
retries += 1
print("Retries:", retries)

backoff_seconds = 1
backoff_seconds *= 2
backoff_seconds *= 2
print("Next backoff:", backoff_seconds, "seconds")

message = "Build"
message += " passed"
print(message)
```

## 5. Example 2 — Practical Example: Tracking request statistics

```python
total_requests = 0
failed_requests = 0
total_latency_ms = 0

# Simulate three batches of traffic
total_requests += 1200
failed_requests += 6
total_latency_ms += 1200 * 85

total_requests += 800
failed_requests += 14
total_latency_ms += 800 * 140

total_requests += 1500
failed_requests += 3
total_latency_ms += 1500 * 90

average_latency = total_latency_ms / total_requests
error_rate = failed_requests / total_requests * 100

print("Total requests:", total_requests)
print("Failed requests:", failed_requests)
print("Average latency:", round(average_latency, 1), "ms")
print("Error rate:", round(error_rate, 2), "%")
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `retries += 1` twice → `2`. This is how retry loops count attempts.
- `backoff_seconds *= 2` doubles the wait each time — *exponential backoff* used by AWS SDKs and Kubernetes.
- `message += " passed"` appends text to the string.

**Example 2**
- Three counters start at `0` and are increased batch by batch with `+=`.
- After collecting, we compute averages and percentages — exactly what monitoring agents do.

## 7. Expected Output

**Example 1:**

```text
Retries: 2
Next backoff: 4 seconds
Build passed
```

**Example 2:**

```text
Total requests: 3500
Failed requests: 23
Average latency: 99.7 ms
Error rate: 0.66 %
```

## 8. Common Mistakes

**1. Using a variable before initialising it**

`count += 1` fails with `NameError` if `count` was never set. Start with `count = 0`.

**2. Writing `x++`**

Python has no `++`. `x++` is a `SyntaxError`; use `x += 1`.

**3. `/=` turns ints into floats**

`n = 10; n /= 2` makes `n` equal `5.0`. Use `//=` to keep an integer.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Countdown:** Start with `seconds = 10`. Subtract 3 three times with `-=` and print the value after each step.
- **Task 2 (Medium) — Exponential backoff:** Starting from 1 second, double the delay with `*=` five times and print the delay for each retry attempt. Also keep a running total of waiting time with `+=`.
- **Task 3 (Practical Challenge) — Daily bandwidth meter:** A server transferred 1.2 GB, 3.4 GB, 0.8 GB and 2.6 GB in four time slots. Use `+=` to total the GB, convert to MB with `*=` (1024), then compute what is left of a 10 GB daily quota with `-=`.

## 10. DevOps/MLOps Connection

- **DevOps:** retry counters, exponential backoff, counting errors while scanning logs.
- **Monitoring:** agents accumulate metrics (`bytes_sent += n`) before pushing them to Prometheus.
- **ML:** training loops accumulate loss (`total_loss += batch_loss`) and count correct predictions.

## 11. Interview Questions

**Q1. Does Python support `++`?**

<details><summary>Show answer</summary>

No. Use `x += 1`.

</details>

**Q2. What does `x //= 3` do?**

<details><summary>Show answer</summary>

It replaces `x` with the floor division of `x` by 3.

</details>

**Q3. What is exponential backoff and how would you implement it?**

<details><summary>Show answer</summary>

Waiting progressively longer between retries (1, 2, 4, 8 s...). Implement by multiplying the delay: `delay *= 2` after each failed attempt.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 10 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 009](../../01-python-fundamentals/day-009/README.md) | [📚 Phase 1: Python Fundamentals](../README.md) | [🏠 Home](../../README.md) | [Day 011 ➡](../../01-python-fundamentals/day-011/README.md)
