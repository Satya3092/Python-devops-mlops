# Day 093 — Practice Tasks: Features, Labels, Training Data, and Testing Data

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Pick X and y

**Problem statement:** For `house_prices.csv`, define X as every column except `price` and y as `price`. Print the feature names, X shape and the first 3 labels.

**Input requirements:** No user input required.

**Expected behavior:** 4 features, shape (200, 4).

**Expected output:**

```text
['size_sqft', 'bedrooms', 'age_years', 'distance_km'] (200, 4)
[566400, 324000, 125000]
```

## Task 2 — Medium: Split and verify

**Problem statement:** Split the house data 70/30 with `random_state=7`. Print the sizes, the mean price in each split and verify no index appears in both.

**Input requirements:** No user input required.

**Expected behavior:** 140/60 rows and `overlap: 0`.

**Expected output:**

```text
140 60
mean price train/test: 323616 324063
overlap: 0
```

## Task 3 — Practical Challenge: Leakage detective

**Problem statement:** Add a leaky feature to the failure dataset: `incident_ticket_opened = failure` (only known after a failure!). Train a depth-3 tree with and without it and compare test accuracy. Print a warning explaining why the leaky model would fail in production.

**Input requirements:** No user input required.

**Expected behavior:** Leaky model ≈ 1.0 accuracy; honest model lower; warning printed.

**Expected output:**

```text
honest  test accuracy: 0.840
leaky   test accuracy: 1.000
WARNING: 'incident_ticket_opened' only exists AFTER a failure, so it is unavailable at prediction time. The leaky model's perfect score would collapse in production.
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
