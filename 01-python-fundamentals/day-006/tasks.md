# Day 006 — Practice Tasks: Type Conversion

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Minutes to seconds

**Problem statement:** Ask for a timeout in minutes (may be a decimal, e.g. 2.5) and print it in seconds as an integer.

**Input requirements:** One number.

**Expected behavior:** Prints `Timeout: 150 seconds`.

**Sample input:**

```text
2.5
```

**Expected output:**

```text
Timeout in minutes: 2.5

Timeout: 150 seconds
```

## Task 2 — Medium: Environment flag parser

**Problem statement:** Environment variables are always text. Given `debug_flag = "false"` and `workers = "4"`, convert them correctly to a bool and an int and print the types. Show why `bool("false")` would be wrong.

**Input requirements:** No user input required.

**Expected behavior:** Shows `False <class 'bool'>`, `4 <class 'int'>` and the wrong result `True`.

**Expected output:**

```text
False <class 'bool'>
4 <class 'int'>
Wrong way bool('false') gives: True
```

## Task 3 — Practical Challenge: Bandwidth estimator

**Problem statement:** Ask for a file size in GB and a network speed in Mbps. Calculate the transfer time in minutes (1 GB = 8000 megabits). Print the result rounded to 2 decimals.

**Input requirements:** Two numbers.

**Expected behavior:** Prints `Transfer time: 6.27 minutes`.

**Sample input:**

```text
4.7
100
```

**Expected output:**

```text
File size (GB): 4.7
Speed (Mbps): 100

Transfer time: 6.27 minutes
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
