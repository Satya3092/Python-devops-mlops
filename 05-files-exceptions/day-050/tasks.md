# Day 050 — Practice Tasks: Working with CSV Files

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Write a CSV

**Problem statement:** Write a CSV `courses.csv` with columns `day,topic` for days 46–50 and print it.

**Input requirements:** No user input required.

**Expected behavior:** Header plus five rows.

**Expected output:**

```text
day,topic
46,File Handling Introduction
47,Reading Files
48,Writing Files
49,Append Mode
50,Working with CSV Files
```

## Task 2 — Medium: Average from CSV

**Problem statement:** Create `scores.csv` with columns `student,score` for 5 students, then read it with `DictReader` and print the average and the highest scorer.

**Input requirements:** No user input required.

**Expected behavior:** Average and top student.

**Expected output:**

```text
Average: 82.8
Top: Fatima (94)
```

## Task 3 — Practical Challenge: Cost report by environment

**Problem statement:** Using the `../../datasets/servers.csv` file from the repository, read every server with `DictReader`, group by `environment`, and write `env_summary.csv` with columns `environment,servers,avg_cpu,critical_count`. Print the summary file.

**Input requirements:** No user input required.

**Expected behavior:** Summary rows for prod, staging and dev.

**Expected output:**

```text
environment,servers,avg_cpu,critical_count
staging,7,59.4,2
dev,7,54.0,1
prod,6,49.0,1
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
