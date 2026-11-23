# Day 050 — Working with CSV Files

[⬅ Day 049](../../05-files-exceptions/day-049/README.md) | [📚 Phase 5: File Handling and Error Handling](../README.md) | [🏠 Home](../../README.md) | [Day 051 ➡](../../05-files-exceptions/day-051/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 5 — File Handling and Error Handling | 🟡 Intermediate | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Read CSV files with `csv.reader` and `csv.DictReader`
- Write CSV files with `csv.writer` and `csv.DictWriter`
- Convert CSV values to the right types

## 2. Topic Explanation

**CSV** (Comma-Separated Values) is the universal table format: exported from Excel, databases, AWS Cost Explorer, monitoring tools...

```
hostname,env,cpu
web-01,prod,45
```

Python's built-in `csv` module handles the tricky parts (quotes, commas inside values):

- `csv.reader(f)` → each row is a **list** of strings.
- `csv.DictReader(f)` → each row is a **dict** using the header as keys (most readable).
- `csv.writer(f).writerow([...])` and `csv.DictWriter(f, fieldnames=[...])` for writing.

Always open CSV files with `newline=""` (prevents blank lines on Windows) and `encoding="utf-8"`.

All values come back as **strings** — convert numbers with `int()`/`float()`.

For heavy analysis you'll use Pandas (Day 86), but the `csv` module needs no installation and is perfect for scripts.

> Run the examples from inside this day's folder (`cd` into it first) so the relative file paths work.

## 3. Syntax

```python
import csv

with open("data.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        print(row["column_name"])

with open("out.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["a", "b"])
    writer.writeheader()
    writer.writerow({"a": 1, "b": 2})
```

| Part | Meaning |
|---|---|
| `csv.reader` | Rows as lists. |
| `csv.DictReader` | Rows as dicts keyed by the header. |
| `csv.DictWriter` | Write dicts; `writeheader()` writes the header row. |
| `newline=""` | Required for correct line endings. |

## 4. Example 1 — Basic Example: Writing and reading a CSV file

```python
import csv

rows = [
    ["name", "role", "city"],
    ["Asha", "DevOps Engineer", "Pune"],
    ["Ravi", "SRE", "Bengaluru"],
    ["Meera", "ML Engineer", "Hyderabad, Telangana"],   # contains a comma!
]

with open("team.csv", "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows(rows)

with open("team.csv", encoding="utf-8") as f:
    print("Raw file:")
    print(f.read(), end="")

with open("team.csv", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)
    print("Header:", header)
    for row in reader:
        print(row)
```

## 5. Example 2 — Practical Example: Server utilisation report from a CSV

```python
import csv

servers = [
    {"hostname": "web-01", "env": "prod", "cpu": 45, "memory": 62, "monthly_cost": 70.08},
    {"hostname": "web-02", "env": "prod", "cpu": 91, "memory": 88, "monthly_cost": 70.08},
    {"hostname": "db-01", "env": "prod", "cpu": 58, "memory": 93, "monthly_cost": 280.32},
    {"hostname": "test-01", "env": "dev", "cpu": 3, "memory": 10, "monthly_cost": 140.16},
]
with open("servers.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(servers[0].keys()))
    writer.writeheader()
    writer.writerows(servers)

# Read it back as dicts and analyse
alerts, idle = [], []
total_cost = 0.0
with open("servers.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        cpu, memory = int(row["cpu"]), int(row["memory"])
        cost = float(row["monthly_cost"])
        total_cost += cost
        if cpu > 85 or memory > 90:
            alerts.append({"hostname": row["hostname"], "cpu": cpu, "memory": memory})
        if cpu < 5:
            idle.append((row["hostname"], cost))

print(f"Total monthly cost: ${total_cost:.2f}")
print("Idle servers (save money):", idle)

with open("alerts.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["hostname", "cpu", "memory"])
    writer.writeheader()
    writer.writerows(alerts)

with open("alerts.csv", encoding="utf-8") as f:
    print("alerts.csv:")
    print(f.read(), end="")
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `writerows` writes a list of lists. The value with a comma is automatically wrapped in quotes in the file.
- `next(reader)` reads the header row; the loop gets the remaining rows as lists.

**Example 2**
- `DictWriter` needs `fieldnames`; `writeheader()` writes them as the first row.
- `DictReader` returns each row as a dict, so we use readable keys like `row["cpu"]`.
- Values are strings, so we convert with `int()`/`float()` before comparing or summing.
- The results are written to a new CSV — a typical *read → filter → write* job.

## 7. Expected Output

**Example 1:**

```text
Raw file:
name,role,city
Asha,DevOps Engineer,Pune
Ravi,SRE,Bengaluru
Meera,ML Engineer,"Hyderabad, Telangana"
Header: ['name', 'role', 'city']
['Asha', 'DevOps Engineer', 'Pune']
['Ravi', 'SRE', 'Bengaluru']
['Meera', 'ML Engineer', 'Hyderabad, Telangana']
```

**Example 2:**

```text
Total monthly cost: $560.64
Idle servers (save money): [('test-01', 140.16)]
alerts.csv:
hostname,cpu,memory
web-02,91,88
db-01,58,93
```

## 8. Common Mistakes

**1. Splitting CSV lines with `split(",")`**

This breaks on quoted values like `"Hyderabad, Telangana"`. Use the `csv` module.

**2. Forgetting `newline=""`**

On Windows you get blank lines between rows.

**3. Comparing strings as numbers**

`row["cpu"] > "85"` compares text. Convert to `int` first.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Write a CSV:** Write a CSV `courses.csv` with columns `day,topic` for days 46–50 and print it.
- **Task 2 (Medium) — Average from CSV:** Create `scores.csv` with columns `student,score` for 5 students, then read it with `DictReader` and print the average and the highest scorer.
- **Task 3 (Practical Challenge) — Cost report by environment:** Using the `../../datasets/servers.csv` file from the repository, read every server with `DictReader`, group by `environment`, and write `env_summary.csv` with columns `environment,servers,avg_cpu,critical_count`. Print the summary file.

## 10. DevOps/MLOps Connection

- **DevOps:** inventory exports, CMDB data, on-call schedules, test results.
- **Cloud:** AWS Cost and Usage Reports and billing exports are CSV — Python summarises them quickly.
- **Data engineering:** CSV is the most common raw data format in ETL.
- **ML:** most beginner datasets (and many real ones) are CSV files loaded into Pandas.

## 11. Interview Questions

**Q1. Why use the `csv` module instead of `split(',')`?**

<details><summary>Show answer</summary>

It correctly handles quoted fields, embedded commas, newlines inside fields and different dialects.

</details>

**Q2. What is the difference between `csv.reader` and `csv.DictReader`?**

<details><summary>Show answer</summary>

`reader` yields lists; `DictReader` yields dicts keyed by the header row.

</details>

**Q3. Why open CSV files with `newline=''`?**

<details><summary>Show answer</summary>

So the csv module controls line endings; otherwise extra blank lines appear on Windows.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 50 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 049](../../05-files-exceptions/day-049/README.md) | [📚 Phase 5: File Handling and Error Handling](../README.md) | [🏠 Home](../../README.md) | [Day 051 ➡](../../05-files-exceptions/day-051/README.md)
