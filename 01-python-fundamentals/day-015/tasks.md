# Day 015 — Practice Tasks: Python Fundamentals Revision and Mini Project

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Unit converter

**Problem statement:** Ask for a size in megabytes and print it in GB (2 decimals) and in bytes (integer). If the size is above 1024 MB also print `Large file`.

**Input requirements:** One number.

**Expected behavior:** Prints 2.0 GB, 2147483648 bytes and `Large file`.

**Sample input:**

```text
2048
```

**Expected output:**

```text
Size in MB: 2048

Size in GB: 2.0
Size in bytes: 2147483648
Large file
```

## Task 2 — Medium: Login validator

**Problem statement:** Ask for a username and an age. Print `Access granted` if the username is not empty and the age is between 18 and 65 inclusive. Otherwise print the exact reason (empty username / age out of range).

**Input requirements:** Two lines.

**Expected behavior:** Prints `Access denied: age out of range`.

**Sample input:**

```text
ravi
17
```

**Expected output:**

```text
Username: ravi
Age: 17

Access denied: age out of range
```

## Task 3 — Practical Challenge: Extend the mini project

**Problem statement:** Extend the Server Resource Alert Calculator: also ask for `load_average` and `cpu_cores`. A load per core above 1.0 is WARNING, above 2.0 CRITICAL. Include it in the overall status and print the free disk space in GB.

**Input requirements:** Server name, CPU %, disk total, disk used, load average, cores.

**Expected behavior:** Load per core 2.4 → CRITICAL overall, free disk 80.0 GB.

**Sample input:**

```text
web-07
55
200
120
9.6
4
```

**Expected output:**

```text
Server: web-07
CPU %: 55
Disk total GB: 200
Disk used GB: 120
Load average: 9.6
CPU cores: 4

Server: web-07
CPU: 55.0 % -> OK
Disk: 60.0 % -> OK | free: 80.0 GB
Load per core: 2.4 -> CRITICAL
Overall: CRITICAL
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
