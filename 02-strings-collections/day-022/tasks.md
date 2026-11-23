# Day 022 — Practice Tasks: List Indexing and Slicing

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Head and tail

**Problem statement:** Given `numbers = list(range(1, 21))`, print the first 5, the last 5 and the middle 10 items.

**Input requirements:** No user input required.

**Expected behavior:** Three sub-lists.

**Expected output:**

```text
[1, 2, 3, 4, 5]
[16, 17, 18, 19, 20]
[6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
```

## Task 2 — Medium: Replace a range

**Problem statement:** Given `stages = ["build", "test", "deploy-dev", "deploy-prod"]`, insert `security-scan` and `integration-test` instead of `test` using slice assignment, then delete `deploy-dev`.

**Input requirements:** No user input required.

**Expected behavior:** Prints the new pipeline stages.

**Expected output:**

```text
['build', 'security-scan', 'integration-test', 'deploy-prod']
```

## Task 3 — Practical Challenge: Rolling restart planner

**Problem statement:** Given 11 pod names `pod-1`…`pod-11`, plan a rolling restart where at most 25 % of pods (rounded down, minimum 1) restart at once. Print each wave and the total number of waves.

**Input requirements:** No user input required.

**Expected behavior:** Wave size 2, 6 waves.

**Expected output:**

```text
Wave 1: ['pod-1', 'pod-2']
Wave 2: ['pod-3', 'pod-4']
Wave 3: ['pod-5', 'pod-6']
Wave 4: ['pod-7', 'pod-8']
Wave 5: ['pod-9', 'pod-10']
Wave 6: ['pod-11']
Total waves: 6
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
