# Day 011 — Practice Tasks: Operator Precedence

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Predict then verify

**Problem statement:** Before running, write down your prediction for: `5 + 2 * 3 - 1`, `(5 + 2) * (3 - 1)`, `20 / 4 / 5`, `2 ** 2 ** 3`. Then print each result.

**Input requirements:** No user input required.

**Expected behavior:** Prints 10, 14, 1.0, 256.

**Expected output:**

```text
10
14
1.0
256
```

## Task 2 — Medium: Fix the formula

**Problem statement:** This Celsius→Fahrenheit conversion is buggy: `f = c * 9 / 5 + 32` is fine, but `c = f - 32 * 5 / 9` is wrong. Fix the second formula with parentheses and convert 98.6 °F.

**Input requirements:** No user input required.

**Expected behavior:** Shows the wrong value (≈80.8) and the correct 37.0.

**Expected output:**

```text
Wrong: 80.8
Right: 37.0
```

## Task 3 — Practical Challenge: Weighted health score

**Problem statement:** A server health score = 100 − (cpu × 0.4 + memory × 0.4 + disk × 0.2). For cpu=80, memory=60, disk=50 compute the score, then decide `needs_attention = score < 40 or cpu > 90 and memory > 90` and rewrite it with explicit parentheses.

**Input requirements:** No user input required.

**Expected behavior:** Score 34.0 and needs_attention True in both versions.

**Expected output:**

```text
Health score: 34.0
Needs attention: True
Needs attention (explicit): True
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
