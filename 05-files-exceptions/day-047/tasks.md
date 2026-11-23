# Day 047 — Practice Tasks: Reading Files

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Count lines and words

**Problem statement:** Read `nginx_access.log` and print the number of lines, words and characters (like `wc`).

**Input requirements:** No user input required.

**Expected behavior:** Prints counts similar to `wc nginx_access.log`.

**Expected output:**

```text
lines=6 words=54 chars=439
```

## Task 2 — Medium: Find unique IPs

**Problem statement:** Read `nginx_access.log` and print the sorted set of unique client IPs and how many there are.

**Input requirements:** No user input required.

**Expected behavior:** Four unique IPs.

**Expected output:**

```text
['10.0.0.5', '10.0.0.9', '192.168.1.10', '192.168.1.11']
Unique IPs: 4
```

## Task 3 — Practical Challenge: Endpoint report

**Problem statement:** From `nginx_access.log`, compute for each path: number of requests and number of errors (status ≥ 400). Print a table sorted by requests (descending) and the overall error rate.

**Input requirements:** No user input required.

**Expected behavior:** Table of paths and error rate 50.0%.

**Expected output:**

```text
PATH           REQ  ERR
/index.html      2    0
/api/orders      2    1
/api/login       1    1
/missing         1    1
Error rate: 50.0%
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
