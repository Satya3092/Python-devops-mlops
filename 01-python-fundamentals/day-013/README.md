# Day 013 — if-else

[⬅ Day 012](../../01-python-fundamentals/day-012/README.md) | [📚 Phase 1: Python Fundamentals](../README.md) | [🏠 Home](../../README.md) | [Day 014 ➡](../../01-python-fundamentals/day-014/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 1 — Python Fundamentals | 🟢 Beginner | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Use `else` to handle the 'otherwise' case
- Write one-line conditional expressions (ternary operator)
- Choose between two code paths cleanly

## 2. Topic Explanation

`if` alone handles the "yes" case. `else` handles the "no" case. Exactly **one** of the two blocks runs.

```python
if condition:
    # runs when True
else:
    # runs when False
```

Analogy: a fork in a road — you take the left path **or** the right one, never both.

For simple choices that produce a value, Python has a one-line **conditional expression** (ternary operator):

```python
status = "UP" if response_code == 200 else "DOWN"
```

Read it as plain English: "status is UP if code is 200, else DOWN".

## 3. Syntax

```python
if condition:
    do_this()
else:
    do_that()

value = value_if_true if condition else value_if_false
```

| Part | Meaning |
|---|---|
| `else:` | Block that runs when the `if` condition is False. No condition of its own. |
| `x if c else y` | Conditional expression: returns `x` when `c` is True, otherwise `y`. |

## 4. Example 1 — Basic Example: Even or odd

```python
number = 7

if number % 2 == 0:
    print(number, "is even")
else:
    print(number, "is odd")

label = "even" if number % 2 == 0 else "odd"
print("Using a conditional expression:", label)
```

## 5. Example 2 — Practical Example: Deployment gate

```python
branch = input("Branch name: ")
tests_passed = input("Did tests pass? (yes/no): ").strip().lower() == "yes"

if branch == "main":
    target = "production"
else:
    target = "preview"

if tests_passed:
    print("Tests passed. Deploying to", target)
else:
    print("Tests failed. Deployment blocked!")

exit_code = 0 if tests_passed else 1
print("Pipeline exit code:", exit_code)
```

*This example asks for input. In the expected output below, the typed values appear after each prompt.*

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `number % 2 == 0` is False for 7, so the `else` block runs.
- The conditional expression produces the same answer in one line.

**Example 2**
- `.strip().lower()` cleans the answer (removes spaces, makes lowercase) so `" YES "` also works (string methods: Day 19).
- The first `if/else` picks a target environment; the second decides whether to deploy.
- `exit_code` mimics how CI tools decide pass/fail: 0 = success, non-zero = failure.

## 7. Expected Output

**Example 1:**

```text
7 is odd
Using a conditional expression: odd
```

**Example 2:**

```text
Branch name: main
Did tests pass? (yes/no): no
Tests failed. Deployment blocked!
Pipeline exit code: 1
```

## 8. Common Mistakes

**1. Giving `else` a condition**

`else cpu < 80:` is a `SyntaxError`. Use `elif` (Day 14) when you need another condition.

**2. Misaligned `else`**

`else` must be at the same indentation level as its `if`.

**3. Overusing ternaries**

Nested conditional expressions are hard to read. Use them only for simple value choices.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Pass or fail:** Ask for an exam score and print `Pass` if it is 50 or more, otherwise `Fail`.
- **Task 2 (Medium) — Service status:** Given `http_code = 503`, use a conditional expression to set `status` to `UP` for 200 and `DOWN` otherwise, then print it. Then use if/else to print an action (`No action` or `Restart service`).
- **Task 3 (Practical Challenge) — Auto-scaling decision:** Ask for the average CPU % of a cluster and the current number of nodes. If CPU > 70, scale out by 1 node (max 10); else, scale in by 1 (min 2). Print the new node count and the reason.

## 10. DevOps/MLOps Connection

- **CI/CD:** pass/fail gates, choosing a target environment from the branch name.
- **Cloud:** auto-scaling logic (scale out else scale in) is an if/else with limits.
- **MLOps:** "If the new model beats the baseline, promote it; else keep the old one and notify the team."

## 11. Interview Questions

**Q1. What is a conditional expression in Python?**

<details><summary>Show answer</summary>

A one-line if/else that returns a value: `a if condition else b`.

</details>

**Q2. Can `else` exist without `if`?**

<details><summary>Show answer</summary>

Not in an if-statement. (`else` can also follow `for`/`while`/`try`, which you will meet later.)

</details>

**Q3. How many blocks of an if/else run?**

<details><summary>Show answer</summary>

Exactly one.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 13 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 012](../../01-python-fundamentals/day-012/README.md) | [📚 Phase 1: Python Fundamentals](../README.md) | [🏠 Home](../../README.md) | [Day 014 ➡](../../01-python-fundamentals/day-014/README.md)
