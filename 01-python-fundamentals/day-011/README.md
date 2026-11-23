# Day 011 — Operator Precedence

[⬅ Day 010](../../01-python-fundamentals/day-010/README.md) | [📚 Phase 1: Python Fundamentals](../README.md) | [🏠 Home](../../README.md) | [Day 012 ➡](../../01-python-fundamentals/day-012/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 1 — Python Fundamentals | 🟢 Beginner | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Predict the order in which Python evaluates an expression
- Use parentheses to make the order explicit
- Avoid common precedence bugs with `not`, `and`, `or`

## 2. Topic Explanation

When an expression has several operators, Python follows **precedence** rules (like BODMAS/PEMDAS in school maths). Highest first:

| Priority | Operators |
|---|---|
| 1 | `( )` parentheses |
| 2 | `**` exponent (right to left) |
| 3 | unary `-x`, `+x` |
| 4 | `* / // %` |
| 5 | `+ -` |
| 6 | comparisons `== != < > <= >= in is` |
| 7 | `not` |
| 8 | `and` |
| 9 | `or` |

Operators with the same priority are evaluated **left to right** (except `**`, which goes right to left).

Golden rule: **when in doubt, add parentheses.** They cost nothing and make the code readable for teammates.

## 3. Syntax

```python
result = a + b * c          # b * c first
result = (a + b) * c        # a + b first
check  = x > 5 and y < 3 or z    # ((x > 5) and (y < 3)) or z
```

| Part | Meaning |
|---|---|
| `( )` | Forces evaluation order; highest priority. |
| `**` | Evaluated before multiplication; right-associative: `2 ** 3 ** 2` = `2 ** 9`. |
| `* / // %` | Evaluated before `+` and `-`. |
| `not > and > or` | Order of logical operators. |

## 4. Example 1 — Basic Example: Seeing precedence in action

```python
print("2 + 3 * 4     =", 2 + 3 * 4)
print("(2 + 3) * 4   =", (2 + 3) * 4)
print("2 ** 3 ** 2   =", 2 ** 3 ** 2)
print("(2 ** 3) ** 2 =", (2 ** 3) ** 2)
print("-3 ** 2       =", -3 ** 2)
print("(-3) ** 2     =", (-3) ** 2)
print("10 - 4 - 3    =", 10 - 4 - 3)
print("100 / 10 * 2  =", 100 / 10 * 2)
```

## 5. Example 2 — Practical Example: Correct average and alert logic

```python
web_01_cpu = 70
web_02_cpu = 90

wrong_average = web_01_cpu + web_02_cpu / 2      # bug!
right_average = (web_01_cpu + web_02_cpu) / 2
print("Wrong average:", wrong_average)
print("Right average:", right_average)

is_prod = False
cpu_high = True
disk_high = True
# Without parentheses: (is_prod and cpu_high) or disk_high
alert_unclear = is_prod and cpu_high or disk_high
# Intended: only alert for production
alert_correct = is_prod and (cpu_high or disk_high)
print("Alert (no parentheses):", alert_unclear)
print("Alert (with parentheses):", alert_correct)
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- Multiplication happens before addition: `2 + 12 = 14`.
- `**` is right-associative: `2 ** 3 ** 2` = `2 ** 9` = 512.
- `-3 ** 2` is `-(3 ** 2)` = -9, because `**` binds tighter than unary minus.
- `10 - 4 - 3` is evaluated left to right: `(10 - 4) - 3`.

**Example 2**
- Without parentheses only `web_02_cpu` is divided, giving a nonsense 115.0 % average.
- `and` binds tighter than `or`, so the unclear version fires an alert for a non-production server. Parentheses express the real intent.

## 7. Expected Output

**Example 1:**

```text
2 + 3 * 4     = 14
(2 + 3) * 4   = 20
2 ** 3 ** 2   = 512
(2 ** 3) ** 2 = 64
-3 ** 2       = -9
(-3) ** 2     = 9
10 - 4 - 3    = 3
100 / 10 * 2  = 20.0
```

**Example 2:**

```text
Wrong average: 115.0
Right average: 80.0
Alert (no parentheses): True
Alert (with parentheses): False
```

## 8. Common Mistakes

**1. Averages without parentheses**

`a + b / 2` is not the average. Write `(a + b) / 2`.

**2. Mixing `and`/`or` without parentheses**

`a or b and c` means `a or (b and c)`. Be explicit.

**3. Negative numbers and powers**

`-2 ** 2` is `-4`. Use `(-2) ** 2` for 4.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Predict then verify:** Before running, write down your prediction for: `5 + 2 * 3 - 1`, `(5 + 2) * (3 - 1)`, `20 / 4 / 5`, `2 ** 2 ** 3`. Then print each result.
- **Task 2 (Medium) — Fix the formula:** This Celsius→Fahrenheit conversion is buggy: `f = c * 9 / 5 + 32` is fine, but `c = f - 32 * 5 / 9` is wrong. Fix the second formula with parentheses and convert 98.6 °F.
- **Task 3 (Practical Challenge) — Weighted health score:** A server health score = 100 − (cpu × 0.4 + memory × 0.4 + disk × 0.2). For cpu=80, memory=60, disk=50 compute the score, then decide `needs_attention = score < 40 or cpu > 90 and memory > 90` and rewrite it with explicit parentheses.

## 10. DevOps/MLOps Connection

- **Monitoring:** composite health scores and SLO burn-rate formulas need correct precedence — a misplaced parenthesis silently produces wrong alerts.
- **Cost / capacity formulas** in automation scripts.
- **ML:** formulas for normalisation `(x - mean) / std` and metrics like F1 = `2 * (p * r) / (p + r)` depend on parentheses.

## 11. Interview Questions

**Q1. What is operator precedence?**

<details><summary>Show answer</summary>

The rules that decide which operator is evaluated first in an expression with several operators.

</details>

**Q2. What is the value of `2 ** 3 ** 2`?**

<details><summary>Show answer</summary>

512, because `**` is right-associative.

</details>

**Q3. Which binds tighter: `and` or `or`?**

<details><summary>Show answer</summary>

`and`. `a or b and c` is `a or (b and c)`.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 11 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 010](../../01-python-fundamentals/day-010/README.md) | [📚 Phase 1: Python Fundamentals](../README.md) | [🏠 Home](../../README.md) | [Day 012 ➡](../../01-python-fundamentals/day-012/README.md)
