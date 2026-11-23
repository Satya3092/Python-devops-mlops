# Day 008 — Comparison Operators

[⬅ Day 007](../../01-python-fundamentals/day-007/README.md) | [📚 Phase 1: Python Fundamentals](../README.md) | [🏠 Home](../../README.md) | [Day 009 ➡](../../01-python-fundamentals/day-009/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 1 — Python Fundamentals | 🟢 Beginner | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Compare values with `== != > < >= <=`
- Understand that comparisons return `True` or `False`
- Use chained comparisons and compare strings

## 2. Topic Explanation

**Comparison operators** ask a yes/no question about two values. The answer is always a boolean: `True` or `False`.

| Operator | Question |
|---|---|
| `==` | Equal? |
| `!=` | Not equal? |
| `>` / `<` | Greater / less than? |
| `>=` / `<=` | Greater-or-equal / less-or-equal? |

`=` assigns; `==` compares. Mixing them up is the #1 beginner mistake.

Python allows **chained comparisons** like maths: `60 <= cpu < 80` means "cpu is at least 60 and below 80".

Strings are compared **alphabetically** (by character codes), and comparison is **case-sensitive**: `"Prod" == "prod"` is `False`.

You already know these from Bash `test`: `-eq`, `-ne`, `-gt`. Python simply uses symbols.

## 3. Syntax

```python
value1 == value2      value1 != value2
value1 >  value2      value1 <  value2
value1 >= value2      value1 <= value2
low <= value < high   # chained
```

| Part | Meaning |
|---|---|
| `==` | True if both values are equal. |
| `!=` | True if values differ. |
| `> < >= <=` | Ordering comparisons. |
| `a <= x < b` | Chained comparison: both conditions must be true. |

## 4. Example 1 — Basic Example: Basic comparisons

```python
cpu = 75
print("cpu == 75:", cpu == 75)
print("cpu != 75:", cpu != 75)
print("cpu > 80:", cpu > 80)
print("cpu <= 80:", cpu <= 80)
print("60 <= cpu < 80:", 60 <= cpu < 80)
print("'prod' == 'Prod':", "prod" == "Prod")
print("'apple' < 'banana':", "apple" < "banana")
```

## 5. Example 2 — Practical Example: Health-check thresholds

```python
CPU_LIMIT = 80
MEMORY_LIMIT = 90
EXPECTED_VERSION = "1.4.2"

cpu_usage = 83
memory_usage = 64
deployed_version = "1.4.1"
http_status = 200

cpu_alert = cpu_usage > CPU_LIMIT
memory_alert = memory_usage >= MEMORY_LIMIT
version_drift = deployed_version != EXPECTED_VERSION
is_success = 200 <= http_status < 300

print("CPU alert:", cpu_alert)
print("Memory alert:", memory_alert)
print("Version drift detected:", version_drift)
print("HTTP success:", is_success)
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- Each `print` shows the result of a comparison — always `True` or `False`.
- `"prod" == "Prod"` is `False` because `p` and `P` are different characters.
- `"apple" < "banana"` is `True` because `a` comes before `b`.

**Example 2**
- Results of comparisons are stored in variables (`cpu_alert`, ...). These booleans will drive `if` statements on Day 12.
- `200 <= http_status < 300` checks for any 2xx success status in one readable expression.

## 7. Expected Output

**Example 1:**

```text
cpu == 75: True
cpu != 75: False
cpu > 80: False
cpu <= 80: True
60 <= cpu < 80: True
'prod' == 'Prod': False
'apple' < 'banana': True
```

**Example 2:**

```text
CPU alert: True
Memory alert: False
Version drift detected: True
HTTP success: True
```

## 8. Common Mistakes

**1. Using `=` instead of `==`**

`if cpu = 80:` is a `SyntaxError`. Use `==` to compare.

**2. Comparing numbers stored as text**

`"10" > "9"` is `False` because text is compared character by character (`'1' < '9'`). Convert to `int` first.

**3. Exact equality with floats**

`0.1 + 0.2 == 0.3` is `False` due to floating-point precision. Use `round()` or `math.isclose()`.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Port checks:** Given `port = 22`, print whether it equals 22, is a privileged port (< 1024), and is not 80.
- **Task 2 (Medium) — Version comparison trap:** Compare `"10"` and `"9"` as strings and as integers. Print both results and a sentence explaining the difference.
- **Task 3 (Practical Challenge) — SLA checker:** An SLA requires uptime >= 99.9 %, average latency < 200 ms and error rate <= 1 %. Given `uptime = 99.95`, `latency_ms = 215`, `error_rate = 0.4`, store each check in a boolean variable and print them plus an overall result using `and` (preview of Day 9).

## 10. DevOps/MLOps Connection

- **DevOps / Monitoring:** every alert rule is a comparison: `cpu > 80`, `disk_free < 10`, `status != "Running"`.
- **CI/CD:** quality gates compare test coverage or vulnerability counts against thresholds.
- **ML / MLOps:** model promotion compares metrics: `new_accuracy > current_accuracy`. Data validation checks `0 <= age <= 120`.

## 11. Interview Questions

**Q1. What is the difference between `=` and `==`?**

<details><summary>Show answer</summary>

`=` assigns a value to a name; `==` compares two values and returns a bool.

</details>

**Q2. What does `1 < x < 10` mean in Python?**

<details><summary>Show answer</summary>

A chained comparison equivalent to `1 < x and x < 10`.

</details>

**Q3. Why is `0.1 + 0.2 == 0.3` False?**

<details><summary>Show answer</summary>

Floats are stored in binary and cannot represent 0.1 exactly. Use `math.isclose()` for float comparisons.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 8 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 007](../../01-python-fundamentals/day-007/README.md) | [📚 Phase 1: Python Fundamentals](../README.md) | [🏠 Home](../../README.md) | [Day 009 ➡](../../01-python-fundamentals/day-009/README.md)
