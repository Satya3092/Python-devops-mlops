# Day 024 — Practice Tasks: Tuples

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Coordinates

**Problem statement:** Store the latitude and longitude of a data centre `(19.07, 72.87)` in a tuple, unpack it and print a sentence with both values.

**Input requirements:** No user input required.

**Expected behavior:** Prints `Data centre at lat 19.07, lon 72.87`.

**Expected output:**

```text
Data centre at lat 19.07, lon 72.87
```

## Task 2 — Medium: Version tuple comparison

**Problem statement:** Convert version strings `"1.10.2"` and `"1.9.8"` to tuples of ints and compare them. Print which is newer.

**Input requirements:** No user input required.

**Expected behavior:** Prints `(1, 10, 2) is newer than (1, 9, 8)`.

**Expected output:**

```text
(1, 10, 2) is newer than (1, 9, 8)
```

<details><summary>💡 Hint</summary>

Tuples compare item by item.

</details>

## Task 3 — Practical Challenge: Server inventory report

**Problem statement:** Given inventory records `(hostname, ip, cpu_cores, memory_gb, role)` for 4 servers, print a table, the total CPU cores and memory, and the hostnames of all `db` servers. Use unpacking in the loop and `*_` to ignore fields you do not need in the second loop.

**Input requirements:** No user input required.

**Expected behavior:** Table, totals and the db hostnames.

**Expected output:**

```text
web-01   10.0.1.10      4 cores   8 GB  web
web-02   10.0.1.11      4 cores   8 GB  web
db-01    10.0.2.10     16 cores  64 GB  db
db-02    10.0.2.11     16 cores  64 GB  db
Total: 40 cores, 144 GB
DB servers: ['db-01', 'db-02']
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
