# Day 021 — Practice Tasks: Lists

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Team list

**Problem statement:** Create a list of 3 team members, add 2 more, replace the second one, remove the last one and print the final list and its length.

**Input requirements:** No user input required.

**Expected behavior:** Shows the modified list and length 4.

**Expected output:**

```text
['Asha', 'Karan', 'Meera', 'John']
Members: 4
```

## Task 2 — Medium: Port audit

**Problem statement:** Given open ports `[22, 80, 443, 3306, 8080, 22]`, print how many there are, the highest port, whether 3306 (MySQL) is exposed and a sorted list without changing the original.

**Input requirements:** No user input required.

**Expected behavior:** Count 6, highest 8080, MySQL exposed True, sorted list.

**Expected output:**

```text
Count: 6
Highest: 8080
MySQL exposed: True
Sorted: [22, 22, 80, 443, 3306, 8080]
Original: [22, 80, 443, 3306, 8080, 22]
```

## Task 3 — Practical Challenge: Build durations report

**Problem statement:** Given CI build durations in seconds `[312, 298, 1045, 305, 287, 330, 299]`, print min, max, average (1 decimal), and a list of builds slower than 1.5 × the average. Then remove those outliers into a new list and print the new average.

**Input requirements:** No user input required.

**Expected behavior:** Identifies 1045 as an outlier and prints the cleaner average.

**Expected output:**

```text
min=287 max=1045 avg=410.9
Outliers: [1045]
Average without outliers: 305.2
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
