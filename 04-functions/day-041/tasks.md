# Day 041 — Practice Tasks: Variable-Length Arguments (*args)

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Average of any numbers

**Problem statement:** Write `average(*values)` that returns the average, or `None` if no values were given. Test with (4, 8, 15), (10,), and no values.

**Input requirements:** No user input required.

**Expected behavior:** 9.0, 10.0, None.

**Expected output:**

```text
9.0
10.0
None
```

## Task 2 — Medium: Build a path

**Problem statement:** Write `build_path(*parts)` that joins any number of parts with `/` and makes sure the result starts with exactly one `/` (strip extra slashes from parts).

**Input requirements:** No user input required.

**Expected behavior:** `build_path("var", "/log/", "nginx")` → `/var/log/nginx`.

**Expected output:**

```text
/var/log/nginx
/etc/systemd/system/app.service
```

## Task 3 — Practical Challenge: Multi-service health summary

**Problem statement:** Write `health_summary(title, *statuses)` where each status is a tuple `(service, code)`. Print a titled table, count healthy (2xx) vs unhealthy, and return the list of unhealthy services. Call it with 5 services, unpacking a list.

**Input requirements:** No user input required.

**Expected behavior:** Table, counts, returned list of unhealthy services.

**Expected output:**

```text
== Production health ==
auth        200  healthy
orders      503  UNHEALTHY
search      200  healthy
payments    500  UNHEALTHY
cart        204  healthy
Healthy: 3 | Unhealthy: 2
Returned: ['orders', 'payments']
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
