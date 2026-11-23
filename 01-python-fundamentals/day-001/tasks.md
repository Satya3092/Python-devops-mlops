# Day 001 — Practice Tasks: Introduction to Python, Installation, IDE, First Program

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Introduce yourself

**Problem statement:** Write a program that prints your name, your current role and why you are learning Python, each on its own line.

**Input requirements:** No user input required.

**Expected behavior:** Three separate lines are printed.

**Expected output:**

```text
Name: Satya
Role: DevOps Engineer
Goal: Learn Python to automate DevOps work and move into MLOps
```

<details><summary>💡 Hint</summary>

Use three `print()` calls.

</details>

## Task 2 — Medium: Server welcome banner

**Problem statement:** Print a login banner (like `/etc/motd`) for a server named `prod-web-01` that is surrounded by lines of 30 `*` characters.

**Input requirements:** No user input required.

**Expected behavior:** A line of stars, the server name, a warning line, then another line of stars.

**Expected output:**

```text
******************************
  Server: prod-web-01
  Authorized access only!
******************************
```

<details><summary>💡 Hint</summary>

`"*" * 30`

</details>

## Task 3 — Practical Challenge: Pipeline stage log

**Problem statement:** Simulate the log of a CI pipeline with stages Checkout, Build, Test and Deploy. Print a header, then one line per stage in the form `[stage n/4] Name ... OK`, and a final success message.

**Input requirements:** No user input required.

**Expected behavior:** Six lines that look like real CI output.

**Expected output:**

```text
Pipeline: build-and-deploy
[stage 1/4] Checkout ... OK
[stage 2/4] Build ... OK
[stage 3/4] Test ... OK
[stage 4/4] Deploy ... OK
Pipeline finished successfully
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
