# Day 015 — Python Fundamentals Revision and Mini Project

[⬅ Day 014](../../01-python-fundamentals/day-014/README.md) | [📚 Phase 1: Python Fundamentals](../README.md) | [🏠 Home](../../README.md) | [Day 016 ➡](../../02-strings-collections/day-016/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 1 — Python Fundamentals | 🟢 Beginner | 90–120 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Revise variables, types, operators, input/output and conditions
- Combine all Phase 1 concepts into one working program
- Build the mini project: **Server Resource Alert Calculator**

## 2. Topic Explanation

Congratulations — you finished the fundamentals! Today you combine them into a small but realistic tool.

**Quick revision**

| Concept | Remember |
|---|---|
| Variables | `snake_case`, constants in `UPPER_CASE` |
| Types | `int`, `float`, `str`, `bool`, `None`, collections |
| Input/Output | `input()` returns `str`; `print(sep=, end=)` |
| Conversion | `int()`, `float()`, `str()`; careful with `bool("False")` |
| Operators | arithmetic → comparison → `not` → `and` → `or` |
| Conditions | `if` / `elif` / `else`, strictest first |

**Mini project: Server Resource Alert Calculator**

The program asks for a server's details (name, total & used memory, total & used disk, CPU %), then:
1. Calculates memory and disk usage percentages.
2. Classifies each resource as OK / WARNING / CRITICAL.
3. Decides an overall status (worst of the three).
4. Prints a formatted report and a recommended action.

This is the seed of the full monitoring tool you will build on Day 75.

## 3. Syntax

```python
# Pattern used in the project
value = float(input("Prompt: "))          # input + conversion
percent = used / total * 100              # arithmetic
if percent >= CRITICAL: ...               # classification
elif percent >= WARNING: ...
else: ...
```

| Part | Meaning |
|---|---|
| `float(input())` | Read a number from the user. |
| `used / total * 100` | Percentage calculation. |
| `CRITICAL / WARNING` | Threshold constants defined once at the top. |
| `if / elif / else` | Classification into levels. |

## 4. Example 1 — Basic Example: Revision: all basics in one place

```python
APP_NAME = "inventory-service"      # constant (str)
replicas = 3                        # int
cpu_limit = 0.5                     # float
is_public = False                   # bool

total_cpu = replicas * cpu_limit
print("App:", APP_NAME)
print("Total CPU requested:", total_cpu, "cores")
print("Type of total_cpu:", type(total_cpu).__name__)

if is_public:
    print("Exposed through a LoadBalancer")
else:
    print("Internal service (ClusterIP)")
```

## 5. Example 2 — Practical Example: Mini project — Server Resource Alert Calculator

```python
WARNING_LEVEL = 75
CRITICAL_LEVEL = 90

server_name = input("Server name: ")
cpu_percent = float(input("CPU usage %: "))
memory_total_gb = float(input("Total memory (GB): "))
memory_used_gb = float(input("Used memory (GB): "))
disk_total_gb = float(input("Total disk (GB): "))
disk_used_gb = float(input("Used disk (GB): "))

memory_percent = memory_used_gb / memory_total_gb * 100
disk_percent = disk_used_gb / disk_total_gb * 100

# Classify each resource
if cpu_percent >= CRITICAL_LEVEL:
    cpu_status = "CRITICAL"
elif cpu_percent >= WARNING_LEVEL:
    cpu_status = "WARNING"
else:
    cpu_status = "OK"

if memory_percent >= CRITICAL_LEVEL:
    memory_status = "CRITICAL"
elif memory_percent >= WARNING_LEVEL:
    memory_status = "WARNING"
else:
    memory_status = "OK"

if disk_percent >= CRITICAL_LEVEL:
    disk_status = "CRITICAL"
elif disk_percent >= WARNING_LEVEL:
    disk_status = "WARNING"
else:
    disk_status = "OK"

# Overall status = the worst individual status
if "CRITICAL" in (cpu_status, memory_status, disk_status):
    overall = "CRITICAL"
    action = "Page the on-call engineer now."
elif "WARNING" in (cpu_status, memory_status, disk_status):
    overall = "WARNING"
    action = "Create a ticket and watch the trend."
else:
    overall = "OK"
    action = "No action needed."

print()
print("=" * 40)
print("Resource report for", server_name)
print("=" * 40)
print("CPU    :", round(cpu_percent, 1), "% ->", cpu_status)
print("Memory :", round(memory_percent, 1), "% ->", memory_status)
print("Disk   :", round(disk_percent, 1), "% ->", disk_status)
print("-" * 40)
print("Overall:", overall)
print("Action :", action)
```

*This example asks for input. In the expected output below, the typed values appear after each prompt.*

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1** revises constants, types, arithmetic and `if/else` in a Kubernetes-flavoured setting.

**Example 2 (mini project)**
- **Constants** at the top keep thresholds in one place — change them once, the whole program updates.
- **Input + conversion:** every answer is converted with `float()` so we can calculate.
- **Arithmetic:** usage % = used / total × 100.
- **Classification:** three `if/elif/else` blocks give each resource a level. (On Day 36 you will replace this repetition with a function.)
- **Overall status:** `"CRITICAL" in (a, b, c)` checks whether any resource is critical.
- **Report:** `"=" * 40` draws lines; `round(x, 1)` keeps output tidy.

## 7. Expected Output

**Example 1:**

```text
App: inventory-service
Total CPU requested: 1.5 cores
Type of total_cpu: float
Internal service (ClusterIP)
```

**Example 2:**

```text
Server name: prod-db-01
CPU usage %: 68
Total memory (GB): 32
Used memory (GB): 27.5
Total disk (GB): 500
Used disk (GB): 462

========================================
Resource report for prod-db-01
========================================
CPU    : 68.0 % -> OK
Memory : 85.9 % -> WARNING
Disk   : 92.4 % -> CRITICAL
----------------------------------------
Overall: CRITICAL
Action : Page the on-call engineer now.
```

## 8. Common Mistakes

**1. Repeating magic numbers**

Writing `90` in ten places means ten edits when the threshold changes. Use constants.

**2. Not converting input**

Forgetting `float()` gives `TypeError` when dividing. Convert at the moment you read the input.

**3. Dividing by zero**

If total memory is entered as 0 the program crashes. Later (Day 52) you will handle this; for now, validate with an `if`.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Unit converter:** Ask for a size in megabytes and print it in GB (2 decimals) and in bytes (integer). If the size is above 1024 MB also print `Large file`.
- **Task 2 (Medium) — Login validator:** Ask for a username and an age. Print `Access granted` if the username is not empty and the age is between 18 and 65 inclusive. Otherwise print the exact reason (empty username / age out of range).
- **Task 3 (Practical Challenge) — Extend the mini project:** Extend the Server Resource Alert Calculator: also ask for `load_average` and `cpu_cores`. A load per core above 1.0 is WARNING, above 2.0 CRITICAL. Include it in the overall status and print the free disk space in GB.

## 10. DevOps/MLOps Connection

- **DevOps:** This calculator is a manual version of what Nagios/Zabbix/Prometheus alerting does. On Day 69 you will read real values with `psutil` instead of typing them, and on Day 75 you will build a complete monitoring tool.
- **Cloud:** The same thresholds drive CloudWatch alarms and auto-scaling policies.
- **MLOps:** Model monitoring uses the same pattern — compute a metric, compare to thresholds, raise an alert.

## 11. Interview Questions

**Q1. Why should thresholds be constants instead of hard-coded numbers?**

<details><summary>Show answer</summary>

Single source of truth: easier to change, test and read. In production they usually come from config files or environment variables.

</details>

**Q2. How would you avoid a ZeroDivisionError in a percentage calculation?**

<details><summary>Show answer</summary>

Check that the denominator is not zero before dividing (`if total > 0:`), or catch the exception with try/except.

</details>

**Q3. How would you make this calculator run automatically every 5 minutes?**

<details><summary>Show answer</summary>

Replace `input()` with real metrics (psutil), and schedule it with cron, a systemd timer, or a Kubernetes CronJob.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 15 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 014](../../01-python-fundamentals/day-014/README.md) | [📚 Phase 1: Python Fundamentals](../README.md) | [🏠 Home](../../README.md) | [Day 016 ➡](../../02-strings-collections/day-016/README.md)
