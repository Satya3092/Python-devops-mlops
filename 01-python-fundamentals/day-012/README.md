# Day 012 — Conditional Statements (if)

[⬅ Day 011](../../01-python-fundamentals/day-011/README.md) | [📚 Phase 1: Python Fundamentals](../README.md) | [🏠 Home](../../README.md) | [Day 013 ➡](../../01-python-fundamentals/day-013/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 1 — Python Fundamentals | 🟢 Beginner | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Write an `if` statement that runs code only when a condition is True
- Understand indentation and code blocks
- Use truthy/falsy values in conditions

## 2. Topic Explanation

Until now every line ran. **Conditional statements** let your program make decisions.

```python
if condition:
    # this block runs only when condition is True
```

- The line ends with a **colon** `:`.
- The code that belongs to the `if` is **indented** (4 spaces is the standard). Indentation is not decoration in Python — it defines the **block**.
- When the indentation stops, the block has ended.

Analogy: a bouncer at a door. *If* you are on the list, you go in. If not, nothing special happens and the night continues.

Bash equivalent:
```bash
if [ "$cpu" -gt 80 ]; then echo "High"; fi
```

## 3. Syntax

```python
if condition:
    statement_1
    statement_2
statement_after_if   # always runs
```

| Part | Meaning |
|---|---|
| `if` | Keyword that starts the decision. |
| `condition` | Any expression that is True/False (or truthy/falsy). |
| `:` | Required at the end of the `if` line. |
| `indented block` | Statements that run only when the condition is True (4 spaces). |

## 4. Example 1 — Basic Example: A simple if

```python
temperature = 35

if temperature > 30:
    print("It is hot today.")
    print("Remember to drink water.")

print("This line always runs.")
```

## 5. Example 2 — Practical Example: Disk usage alerts

```python
disk_usage = int(input("Disk usage %: "))
log_files = ["app.log", "error.log"]
maintenance_message = ""

if disk_usage >= 80:
    print("WARNING: disk usage is", disk_usage, "%")

if disk_usage >= 95:
    print("CRITICAL: clean up immediately!")

if log_files:                      # a non-empty list is truthy
    print("Log files to rotate:", log_files)

if not maintenance_message:        # empty string is falsy
    print("No maintenance message set.")

print("Check complete.")
```

*This example asks for input. In the expected output below, the typed values appear after each prompt.*

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `temperature > 30` is True, so both indented lines run.
- `print("This line always runs.")` is not indented, so it is outside the `if`.

**Example 2**
- Each `if` is checked independently. 87 passes the first check but not the second.
- `if log_files:` relies on truthiness — a list with items counts as True.
- `if not maintenance_message:` runs because the empty string is falsy.

## 7. Expected Output

**Example 1:**

```text
It is hot today.
Remember to drink water.
This line always runs.
```

**Example 2:**

```text
Disk usage %: 87
WARNING: disk usage is 87 %
Log files to rotate: ['app.log', 'error.log']
No maintenance message set.
Check complete.
```

## 8. Common Mistakes

**1. Forgetting the colon**

`if cpu > 80` → `SyntaxError: expected ':'`.

**2. Inconsistent indentation**

Mixing tabs and spaces or 2 vs 4 spaces gives `IndentationError`. Configure VS Code to insert 4 spaces.

**3. Comparing strings from `input()` to numbers**

`if input() > 80:` → `TypeError`. Convert with `int()` first.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Positive number:** Ask for a number and print `Positive` only if it is greater than 0.
- **Task 2 (Medium) — Weak password warning:** Ask for a password and print a warning if it is shorter than 8 characters (use `len()`), and another warning if it equals `password`.
- **Task 3 (Practical Challenge) — Container restart policy:** Given `restart_count = 6`, `exit_code = 137` and `status = "CrashLoopBackOff"`, write separate `if` statements that print: a restart warning if restarts > 5; `Killed by OOM` if exit_code is 137; and `Pod is crash looping` if the status matches.

## 10. DevOps/MLOps Connection

- **DevOps:** "If the health check fails, roll back." "If the branch is `main`, deploy." Every automation is full of `if`s.
- **Kubernetes:** exit code 137 = OOMKilled, 143 = SIGTERM. Scripts check these codes with `if`.
- **MLOps:** "If the new model's accuracy is better, register it." "If data drift is detected, trigger retraining."

## 11. Interview Questions

**Q1. Why is indentation important in Python?**

<details><summary>Show answer</summary>

Indentation defines code blocks. Python has no braces, so the indentation level decides which statements belong to an `if`, loop or function.

</details>

**Q2. What does `if my_list:` check?**

<details><summary>Show answer</summary>

Whether the list is non-empty (truthy).

</details>

**Q3. What is PEP 8's recommendation for indentation?**

<details><summary>Show answer</summary>

4 spaces per level, no tabs.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 12 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 011](../../01-python-fundamentals/day-011/README.md) | [📚 Phase 1: Python Fundamentals](../README.md) | [🏠 Home](../../README.md) | [Day 013 ➡](../../01-python-fundamentals/day-013/README.md)
