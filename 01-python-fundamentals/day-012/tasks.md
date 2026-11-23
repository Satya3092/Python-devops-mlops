# Day 012 — Practice Tasks: Conditional Statements (if)

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Positive number

**Problem statement:** Ask for a number and print `Positive` only if it is greater than 0.

**Input requirements:** One integer.

**Expected behavior:** Prints `Positive` for 15.

**Sample input:**

```text
15
```

**Expected output:**

```text
Number: 15

Positive
```

## Task 2 — Medium: Weak password warning

**Problem statement:** Ask for a password and print a warning if it is shorter than 8 characters (use `len()`), and another warning if it equals `password`.

**Input requirements:** One line.

**Expected behavior:** Prints the length warning.

**Sample input:**

```text
admin
```

**Expected output:**

```text
Password: admin

Warning: password is shorter than 8 characters
```

## Task 3 — Practical Challenge: Container restart policy

**Problem statement:** Given `restart_count = 6`, `exit_code = 137` and `status = "CrashLoopBackOff"`, write separate `if` statements that print: a restart warning if restarts > 5; `Killed by OOM` if exit_code is 137; and `Pod is crash looping` if the status matches.

**Input requirements:** No user input required.

**Expected behavior:** All three messages are printed.

**Expected output:**

```text
Warning: container restarted 6 times
Killed by OOM (exit code 137) - increase memory limit
Pod is crash looping
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
