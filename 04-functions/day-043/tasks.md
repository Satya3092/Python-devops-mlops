# Day 043 — Practice Tasks: Scope and Local/Global Variables

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Predict the output

**Problem statement:** Without running it, predict what this prints, then verify: `x = 10`, `def f(): x = 20; print(x)`, call `f()`, then `print(x)`.

**Input requirements:** No user input required.

**Expected behavior:** 20 then 10.

**Expected output:**

```text
20
10
```

## Task 2 — Medium: Fix the UnboundLocalError

**Problem statement:** This code fails: `deployments = 0` / `def deploy(): deployments += 1`. Fix it twice: once with `global`, once properly by passing the value in and returning the new value.

**Input requirements:** No user input required.

**Expected behavior:** Both versions reach 2 deployments.

**Expected output:**

```text
global version: 2
pure version: 2
```

## Task 3 — Practical Challenge: Config with constants

**Problem statement:** Define global constants `DEFAULT_REGION` and `ALLOWED_ENVS`. Write a pure function `build_config(env, region=None)` that validates `env` against `ALLOWED_ENVS`, uses `DEFAULT_REGION` if no region is given, and returns a dict — or raises `ValueError` for bad input. Show a success and a failure.

**Input requirements:** No user input required.

**Expected behavior:** A config dict and a ValueError message.

**Expected output:**

```text
{'env': 'prod', 'region': 'ap-south-1'}
ValueError: env must be one of ('dev', 'staging', 'prod'), got 'qa'
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
