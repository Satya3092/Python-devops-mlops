# Day 014 — elif and Nested Conditions

[⬅ Day 013](../../01-python-fundamentals/day-013/README.md) | [📚 Phase 1: Python Fundamentals](../README.md) | [🏠 Home](../../README.md) | [Day 015 ➡](../../01-python-fundamentals/day-015/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 1 — Python Fundamentals | 🟢 Beginner | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Check several conditions in order with `elif`
- Nest `if` statements inside each other
- Use the `in` operator to simplify membership checks

## 2. Topic Explanation

When there are **more than two** possibilities, use `elif` ("else if"). Python checks each condition **top to bottom** and runs the **first** block whose condition is True, then skips the rest.

```python
if cpu >= 90:
    level = "critical"
elif cpu >= 75:
    level = "warning"
else:
    level = "ok"
```

Order matters: put the most specific / highest threshold first.

**Nested conditions** are `if` statements inside other `if` blocks. They model "first check this, then — only if it passed — check that". Keep nesting shallow (2–3 levels); deeper nesting becomes hard to read.

The `in` operator checks membership: `env in ("dev", "staging")` is cleaner than chaining `or`.

## 3. Syntax

```python
if condition_1:
    block_1
elif condition_2:
    block_2
else:
    block_default

if outer_condition:
    if inner_condition:
        block
```

| Part | Meaning |
|---|---|
| `elif` | Another condition, checked only if all previous ones were False. |
| `else` | Optional catch-all when nothing matched. |
| `nested if` | An `if` inside another block — indented one more level. |
| `x in (a, b)` | True if `x` equals any item in the collection. |

## 4. Example 1 — Basic Example: Grading with elif

```python
score = 82

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"

print("Score", score, "-> grade", grade)
```

## 5. Example 2 — Practical Example: Incident severity classifier

```python
environment = "prod"
http_status = 503
error_rate = 12.5

if http_status >= 500:
    if environment == "prod":
        if error_rate > 10:
            severity = "SEV-1 (page on-call now)"
        else:
            severity = "SEV-2 (investigate within 1 hour)"
    elif environment in ("staging", "qa"):
        severity = "SEV-3 (fix during work hours)"
    else:
        severity = "SEV-4 (dev environment, low priority)"
elif http_status >= 400:
    severity = "Client error - check request logs"
else:
    severity = "OK"

print("Environment:", environment, "| Status:", http_status, "| Errors:", error_rate, "%")
print("Severity:", severity)
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- 82 fails `>= 90`, passes `>= 80` → grade B; the remaining `elif`/`else` are skipped.

**Example 2**
- The outer `if/elif/else` splits by status class (5xx, 4xx, other).
- Inside the 5xx branch, a nested `if` looks at the environment, and inside prod another nested `if` looks at the error rate.
- `environment in ("staging", "qa")` checks membership in a tuple.

## 7. Expected Output

**Example 1:**

```text
Score 82 -> grade B
```

**Example 2:**

```text
Environment: prod | Status: 503 | Errors: 12.5 %
Severity: SEV-1 (page on-call now)
```

## 8. Common Mistakes

**1. Wrong order of conditions**

If you test `cpu >= 75` before `cpu >= 90`, a 95 % CPU is labelled *warning*. Put the strictest condition first.

**2. Separate `if`s instead of `elif`**

With separate `if`s, several blocks can run. Use `elif` when only one outcome should happen.

**3. Deep nesting**

More than 3 levels is hard to follow. Combine conditions with `and` or use early exits (functions, Day 38).

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Traffic light:** Ask for a colour (red/yellow/green) and print Stop / Slow down / Go, or `Invalid colour`.
- **Task 2 (Medium) — HTTP status explainer:** Given `status_code = 404`, print the category: 1xx Informational, 2xx Success, 3xx Redirection, 4xx Client Error, 5xx Server Error, otherwise Unknown. Inside 4xx, print a special note for 401 / 403 / 404.
- **Task 3 (Practical Challenge) — Server health classifier:** Ask for CPU %, memory % and disk %. Classify the server as CRITICAL if any value >= 90, WARNING if any >= 75, otherwise HEALTHY. Additionally, if CRITICAL and disk is the cause, print `Suggested action: clean /var/log`.

## 10. DevOps/MLOps Connection

- **Monitoring:** mapping metrics to OK/WARNING/CRITICAL is exactly how Nagios and Prometheus alert levels work.
- **Incident management:** severity classification (SEV-1...SEV-4) is an `if/elif` tree.
- **ML:** converting a predicted probability into risk bands ("high", "medium", "low") for business users.

## 11. Interview Questions

**Q1. What is the difference between multiple `if` statements and `if/elif`?**

<details><summary>Show answer</summary>

With `if/elif`, at most one block runs (the first True). Separate `if`s are each evaluated and several can run.

</details>

**Q2. Is `else` required after `elif`?**

<details><summary>Show answer</summary>

No, it is optional.

</details>

**Q3. How can you reduce deeply nested ifs?**

<details><summary>Show answer</summary>

Combine conditions with `and`, use `in` for membership, return early from functions, or use lookup dictionaries.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 14 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 013](../../01-python-fundamentals/day-013/README.md) | [📚 Phase 1: Python Fundamentals](../README.md) | [🏠 Home](../../README.md) | [Day 015 ➡](../../01-python-fundamentals/day-015/README.md)
