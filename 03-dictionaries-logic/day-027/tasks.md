# Day 027 — Practice Tasks: Dictionary Methods

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Print a dictionary nicely

**Problem statement:** Given `capitals = {"India": "New Delhi", "Japan": "Tokyo", "France": "Paris"}`, print each pair as `Country: Capital` and then all capitals in alphabetical order.

**Input requirements:** No user input required.

**Expected behavior:** Three lines and a sorted list.

**Expected output:**

```text
India: New Delhi
Japan: Tokyo
France: Paris
['New Delhi', 'Paris', 'Tokyo']
```

## Task 2 — Medium: Word frequency

**Problem statement:** Count how many times each word appears in `"deploy test deploy build test deploy"` and print words with counts, most frequent first.

**Input requirements:** No user input required.

**Expected behavior:** deploy 3, test 2, build 1.

**Expected output:**

```text
deploy 3
test 2
build 1
```

## Task 3 — Practical Challenge: HTTP status report

**Problem statement:** Given status codes from an access log `[200, 200, 404, 500, 200, 301, 404, 200, 503, 200]`, count each code, then group counts by class (2xx, 3xx, 4xx, 5xx) into another dict. Print both and the error percentage (4xx + 5xx).

**Input requirements:** No user input required.

**Expected behavior:** 2xx: 5, 3xx: 1, 4xx: 2, 5xx: 2 → 40.0% errors.

**Expected output:**

```text
By code: {200: 5, 404: 2, 500: 1, 301: 1, 503: 1}
By class: {'2xx': 5, '3xx': 1, '4xx': 2, '5xx': 2}
Error percentage: 40.0%
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
