# Day 032 — Break, Continue, and Pass

[⬅ Day 031](../../03-dictionaries-logic/day-031/README.md) | [📚 Phase 3: Dictionaries and Programming Logic](../README.md) | [🏠 Home](../../README.md) | [Day 033 ➡](../../03-dictionaries-logic/day-033/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 3 — Dictionaries and Programming Logic | 🟢 Beginner | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Exit a loop early with `break`
- Skip one iteration with `continue`
- Use `pass` as a placeholder
- Use `for ... else` to detect 'not found'

## 2. Topic Explanation

Three keywords control loop flow:

| Keyword | Effect | Analogy |
|---|---|---|
| `break` | Leave the loop **completely** | Found your keys — stop searching the house |
| `continue` | Skip to the **next** iteration | This room is locked — move to the next room |
| `pass` | Do **nothing** (placeholder) | "TODO" sticky note |

`pass` is needed because Python does not allow an empty block:
```python
if disk_usage > 90:
    pass   # TODO: implement cleanup
```

**`for ... else`**: the `else` block runs only when the loop completes **without** `break`. It is the clean way to say "searched everything and found nothing".

## 3. Syntax

```python
for item in items:
    if skip_condition:
        continue
    if stop_condition:
        break
else:
    # runs only if no break happened
    ...
```

| Part | Meaning |
|---|---|
| `break` | Ends the innermost loop immediately. |
| `continue` | Jumps to the next iteration. |
| `pass` | Empty statement; does nothing. |
| `for ... else` | `else` runs when the loop was not broken. |

## 4. Example 1 — Basic Example: break, continue, pass

```python
for number in range(1, 10):
    if number == 6:
        print("Found 6, stopping")
        break
    if number % 2 == 0:
        continue                 # skip even numbers
    print("Odd number:", number)

for task in ["build", "test", "deploy"]:
    if task == "test":
        pass                     # TODO: add tests later
    print("Running", task)
```

## 5. Example 2 — Practical Example: Scanning logs and searching for a free port

```python
log_lines = [
    "INFO  Service starting",
    "",
    "# this is a comment",
    "INFO  Connected to database",
    "ERROR Out of memory",
    "INFO  This line is never read",
]

for line_number, line in enumerate(log_lines, start=1):
    if not line or line.startswith("#"):
        continue                                  # ignore blank lines and comments
    if line.startswith("ERROR"):
        print(f"First error at line {line_number}: {line}")
        break                                     # stop at the first error
    print(f"line {line_number} ok")

# Find the first free port (for ... else)
used_ports = {8000, 8001, 8002}
for port in range(8000, 8003):
    if port not in used_ports:
        print("Free port found:", port)
        break
else:
    print("No free port between 8000 and 8002")
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- Even numbers trigger `continue`, so only odd numbers print; reaching 6 triggers `break`.
- `pass` keeps the `if` block syntactically valid while doing nothing.

**Example 2**
- `continue` skips empty lines and comments — a pattern used when parsing config files.
- `break` stops reading at the first ERROR (fail-fast).
- All ports 8000–8002 are used, so the loop never breaks and the `else` block reports that nothing was found.

## 7. Expected Output

**Example 1:**

```text
Odd number: 1
Odd number: 3
Odd number: 5
Found 6, stopping
Running build
Running test
Running deploy
```

**Example 2:**

```text
line 1 ok
line 4 ok
First error at line 5: ERROR Out of memory
No free port between 8000 and 8002
```

## 8. Common Mistakes

**1. `break` only exits one loop**

In nested loops, `break` leaves only the innermost loop. Use a flag or a function with `return` to exit several levels.

**2. Leaving `pass` in production code**

`pass` is a placeholder; forgetting to implement the logic hides bugs. Add a TODO comment or raise `NotImplementedError`.

**3. Misreading `for...else`**

The `else` does NOT mean 'if the loop did not run'; it means 'if the loop did not break'.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Stop at negative:** Loop over `[4, 7, 2, -1, 9]` and print numbers until a negative number appears, then print `Stopped at -1`.
- **Task 2 (Medium) — Skip maintenance hosts:** Given hosts `["web-01", "web-02 (maintenance)", "web-03", "db-01 (maintenance)"]`, print `Deploying to <host>` only for hosts not in maintenance and count skipped hosts.
- **Task 3 (Practical Challenge) — Find a healthy replica:** Replicas are checked in order: `[("replica-1", 503), ("replica-2", 500), ("replica-3", 200), ("replica-4", 200)]`. Route traffic to the first replica that returns 200. If none is healthy, print `All replicas down - failing over to DR region`. Test with the given list and with a list where all return 500.

## 10. DevOps/MLOps Connection

- **DevOps:** fail fast on the first error (`break`), skip hosts in maintenance (`continue`), stub out future features (`pass`).
- **Cloud:** search for the first available subnet/AZ; failover logic with `for...else`.
- **ML:** early stopping — `break` out of the training loop when validation loss stops improving.

## 11. Interview Questions

**Q1. What is the difference between `break` and `continue`?**

<details><summary>Show answer</summary>

`break` exits the loop entirely; `continue` skips the rest of the current iteration and moves to the next one.

</details>

**Q2. Why does Python need `pass`?**

<details><summary>Show answer</summary>

Blocks cannot be empty; `pass` is a no-op placeholder that satisfies the syntax.

</details>

**Q3. Explain `for ... else`.**

<details><summary>Show answer</summary>

The `else` block executes after the loop finishes normally; it is skipped if the loop exits via `break`. Useful for search loops.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 32 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 031](../../03-dictionaries-logic/day-031/README.md) | [📚 Phase 3: Dictionaries and Programming Logic](../README.md) | [🏠 Home](../../README.md) | [Day 033 ➡](../../03-dictionaries-logic/day-033/README.md)
