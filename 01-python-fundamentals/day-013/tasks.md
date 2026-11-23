# Day 013 — Practice Tasks: if-else

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Pass or fail

**Problem statement:** Ask for an exam score and print `Pass` if it is 50 or more, otherwise `Fail`.

**Input requirements:** One integer.

**Expected behavior:** Prints `Fail`.

**Sample input:**

```text
42
```

**Expected output:**

```text
Score: 42

Fail
```

## Task 2 — Medium: Service status

**Problem statement:** Given `http_code = 503`, use a conditional expression to set `status` to `UP` for 200 and `DOWN` otherwise, then print it. Then use if/else to print an action (`No action` or `Restart service`).

**Input requirements:** No user input required.

**Expected behavior:** Prints `Status: DOWN` and `Action: Restart service`.

**Expected output:**

```text
Status: DOWN
Action: Restart service
```

## Task 3 — Practical Challenge: Auto-scaling decision

**Problem statement:** Ask for the average CPU % of a cluster and the current number of nodes. If CPU > 70, scale out by 1 node (max 10); else, scale in by 1 (min 2). Print the new node count and the reason.

**Input requirements:** Two integers.

**Expected behavior:** Prints `Scaling out: 4 -> 5 nodes`.

**Sample input:**

```text
78
4
```

**Expected output:**

```text
Average CPU %: 78
Current nodes: 4

Scaling out: 4 -> 5 nodes (CPU 78 % > 70 %)
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
