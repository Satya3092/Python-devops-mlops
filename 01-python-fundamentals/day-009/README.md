# Day 009 — Logical Operators

[⬅ Day 008](../../01-python-fundamentals/day-008/README.md) | [📚 Phase 1: Python Fundamentals](../README.md) | [🏠 Home](../../README.md) | [Day 010 ➡](../../01-python-fundamentals/day-010/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 1 — Python Fundamentals | 🟢 Beginner | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Combine conditions using `and`, `or`, `not`
- Read truth tables
- Understand short-circuit evaluation and truthy/falsy values

## 2. Topic Explanation

Logical operators combine True/False values into a single answer.

| Operator | True when... | Example |
|---|---|---|
| `and` | **both** sides are True | `cpu > 80 and memory > 80` |
| `or` | **at least one** side is True | `env == "prod" or env == "staging"` |
| `not` | flips True ↔ False | `not is_healthy` |

Truth table for `and` / `or`:

| A | B | A and B | A or B |
|---|---|---|---|
| True | True | True | True |
| True | False | False | True |
| False | True | False | True |
| False | False | False | False |

**Short-circuit evaluation:** Python stops as soon as it knows the answer. In `A and B`, if `A` is False, `B` is never evaluated. This is like `cmd1 && cmd2` in Bash.

**Truthy / falsy:** In conditions, `0`, `0.0`, `""`, `[]`, `{}` and `None` behave like `False`; everything else like `True`.

## 3. Syntax

```python
condition1 and condition2
condition1 or condition2
not condition
```

| Part | Meaning |
|---|---|
| `and` | True only if both conditions are True. |
| `or` | True if at least one condition is True. |
| `not` | Reverses a boolean. |
| `( )` | Use parentheses to make complex conditions clear. |

## 4. Example 1 — Basic Example: Truth table in code

```python
print("True and False =", True and False)
print("True or False  =", True or False)
print("not True       =", not True)

is_weekend = False
is_holiday = True
print("Day off?", is_weekend or is_holiday)

print("Empty list is falsy:", not [])
print("'' or 'default' ->", "" or "default")
```

## 5. Example 2 — Practical Example: Deciding when to page the on-call engineer

```python
environment = "prod"
cpu_usage = 92
error_rate = 0.5
in_maintenance_window = False

high_cpu = cpu_usage > 90
high_errors = error_rate > 5
is_production = environment == "prod"

# Page only for production, outside maintenance, if something is wrong
should_page = is_production and not in_maintenance_window and (high_cpu or high_errors)
print("High CPU:", high_cpu, "| High errors:", high_errors)
print("Page on-call engineer?", should_page)

# Safe defaults with 'or'
configured_region = ""
region = configured_region or "us-east-1"
print("Region used:", region)
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- Shows the basic results of `and`, `or` and `not`.
- `not []` is `True` because an empty list is falsy.
- `"" or "default"` returns `"default"`: `or` returns the first truthy value.

**Example 2**
- Three booleans are prepared with comparisons.
- `should_page` combines them; parentheses ensure `high_cpu or high_errors` is evaluated as a group.
- `configured_region or "us-east-1"` is a common idiom to fall back to a default when a setting is empty.

## 7. Expected Output

**Example 1:**

```text
True and False = False
True or False  = True
not True       = False
Day off? True
Empty list is falsy: True
'' or 'default' -> default
```

**Example 2:**

```text
High CPU: True | High errors: False
Page on-call engineer? True
Region used: us-east-1
```

## 8. Common Mistakes

**1. `if env == "prod" or "staging":`**

This is always True because `"staging"` alone is truthy. Write `env == "prod" or env == "staging"` or `env in ("prod", "staging")`.

**2. Using `&&`, `||`, `!`**

Those are Bash/C operators. Python uses the words `and`, `or`, `not`.

**3. Missing parentheses**

`a and b or c` is `(a and b) or c`. Add parentheses when you mean `a and (b or c)`.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Access check:** A user can deploy if `is_admin` is True **or** (`is_developer` is True **and** `environment` is not `prod`). Test with is_admin=False, is_developer=True, environment='staging'.
- **Task 2 (Medium) — Business hours:** Given `hour = 14` and `is_weekday = True`, decide if this is a safe deployment window (weekday, between 10 and 16 inclusive) and print the result. Also print the opposite using `not`.
- **Task 3 (Practical Challenge) — Backup decision:** Run a backup if the disk has more than 20 GB free AND (it is after 01:00 and before 05:00 OR a `force_backup` flag is set) AND no other backup is running. Evaluate for free_gb=35, hour=14, force_backup=True, backup_running=False and explain each part.

## 10. DevOps/MLOps Connection

- **DevOps:** Alerting rules (`cpu > 90 and duration > 5m`), deployment guards (`branch == "main" and tests_passed`) and feature flags all combine conditions.
- **Cloud automation:** "Stop the instance if it is tagged `dev` **and** it is after 8 pm" — a classic cost-saving Lambda.
- **Data / ML:** Filtering rows in Pandas uses the same logic with `&`, `|`, `~` (Day 89).

## 11. Interview Questions

**Q1. What is short-circuit evaluation?**

<details><summary>Show answer</summary>

Python stops evaluating `and`/`or` as soon as the result is known. `False and f()` never calls `f()`.

</details>

**Q2. What does `x or 'default'` return if `x` is an empty string?**

<details><summary>Show answer</summary>

`'default'`, because `or` returns the first truthy operand (or the last operand).

</details>

**Q3. Which values are falsy in Python?**

<details><summary>Show answer</summary>

`False`, `None`, `0`, `0.0`, `''`, and empty collections such as `[]`, `()`, `{}`, `set()`.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 9 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 008](../../01-python-fundamentals/day-008/README.md) | [📚 Phase 1: Python Fundamentals](../README.md) | [🏠 Home](../../README.md) | [Day 010 ➡](../../01-python-fundamentals/day-010/README.md)
