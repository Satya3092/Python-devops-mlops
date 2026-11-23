# Day 035 — Programming Logic Practice and Mini Project

[⬅ Day 034](../../03-dictionaries-logic/day-034/README.md) | [📚 Phase 3: Dictionaries and Programming Logic](../README.md) | [🏠 Home](../../README.md) | [Day 036 ➡](../../04-functions/day-036/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 3 — Dictionaries and Programming Logic | 🟢 Beginner | 90–120 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Combine loops, conditions, lists and dictionaries to solve problems
- Practise breaking a problem into small steps (algorithmic thinking)
- Build the mini project: **Inventory Report Generator**

## 2. Topic Explanation

Programming is mostly **problem decomposition**: turning a vague goal into small, precise steps.

A simple method you can use for every task:

1. **Input** — what data do I have? (a list of dicts? a text?)
2. **Output** — what exactly should be printed/returned?
3. **Steps** — in plain English, how would I do it by hand?
4. **Data structure** — list for ordered items, dict for lookups/counting, set for uniqueness.
5. **Code** it, then **test** with sample data, including edge cases (empty list, missing keys).

**Mini project: Inventory Report Generator.** Given a server inventory (list of dicts), produce:
- servers grouped by environment,
- resource totals per environment,
- servers that violate rules (missing owner tag, too-old OS, high utilisation),
- a final summary.

This mirrors real CMDB/inventory audit scripts.

## 3. Syntax

```python
# Typical shape of a report script
groups = {}
for record in records:                 # loop
    key = record["field"]
    groups.setdefault(key, []).append(record)    # group
problems = [r for r in records if rule(r)]       # filter
```

| Part | Meaning |
|---|---|
| `loop` | Visit every record once. |
| `setdefault().append()` | Group records by a key. |
| `comprehension` | Filter records that break a rule. |
| `f-strings` | Format the final report. |

## 4. Example 1 — Basic Example: Logic practice: FizzBuzz for deployments

```python
# Classic FizzBuzz, DevOps flavour:
# build number divisible by 3 -> "lint", by 5 -> "scan", by both -> "full-pipeline"
for build in range(1, 16):
    if build % 15 == 0:
        print(build, "full-pipeline")
    elif build % 3 == 0:
        print(build, "lint")
    elif build % 5 == 0:
        print(build, "scan")
    else:
        print(build, "build-only")
```

## 5. Example 2 — Practical Example: Mini project — Inventory Report Generator

```python
inventory = [
    {"host": "web-01", "env": "prod", "os": "ubuntu-24.04", "cpu": 4, "ram_gb": 8, "cpu_util": 45, "owner": "team-web"},
    {"host": "web-02", "env": "prod", "os": "ubuntu-20.04", "cpu": 4, "ram_gb": 8, "cpu_util": 91, "owner": "team-web"},
    {"host": "db-01", "env": "prod", "os": "rhel-9", "cpu": 16, "ram_gb": 64, "cpu_util": 62, "owner": "team-data"},
    {"host": "web-01", "env": "staging", "os": "ubuntu-24.04", "cpu": 2, "ram_gb": 4, "cpu_util": 12, "owner": ""},
    {"host": "batch-01", "env": "dev", "os": "ubuntu-18.04", "cpu": 8, "ram_gb": 16, "cpu_util": 5, "owner": "team-ml"},
]
OUTDATED_OS = {"ubuntu-18.04", "ubuntu-20.04"}
HIGH_UTIL = 85

# 1. Group by environment
by_env = {}
for server in inventory:
    by_env.setdefault(server["env"], []).append(server)

# 2. Totals per environment
print("=== Capacity per environment ===")
for env, servers in by_env.items():
    total_cpu = sum(s["cpu"] for s in servers)
    total_ram = sum(s["ram_gb"] for s in servers)
    hosts = ", ".join(s["host"] for s in servers)
    print(f"{env:<8} servers={len(servers)} cpu={total_cpu:<3} ram={total_ram:<3}GB [{hosts}]")

# 3. Rule violations
print("\n=== Violations ===")
violations = []
for s in inventory:
    name = f"{s['env']}/{s['host']}"
    if not s["owner"]:
        violations.append((name, "missing owner tag"))
    if s["os"] in OUTDATED_OS:
        violations.append((name, f"outdated OS {s['os']}"))
    if s["cpu_util"] >= HIGH_UTIL:
        violations.append((name, f"high CPU {s['cpu_util']}%"))
for name, reason in violations:
    print(f"- {name:<16} {reason}")

# 4. Summary
affected = {name for name, _ in violations}
print("\n=== Summary ===")
print(f"Servers: {len(inventory)} | with issues: {len(affected)} | violations: {len(violations)}")
compliance = (len(inventory) - len(affected)) / len(inventory) * 100
print(f"Compliance: {compliance:.0f}%")
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1** practises `%` and `if/elif` ordering: the "divisible by both" case must come first.

**Example 2 (mini project)**
1. **Grouping:** `setdefault(env, []).append(server)` creates a dict of env → list of servers.
2. **Totals:** generator expressions inside `sum()` add CPU and RAM per group; `", ".join(...)` lists hostnames.
3. **Rules:** each rule is a simple `if`. Violations are stored as `(name, reason)` tuples so one server can have several.
4. **Summary:** a set comprehension counts unique affected servers; compliance is a percentage.
- `"\n=== ... ==="` starts a section with an empty line.

## 7. Expected Output

**Example 1:**

```text
1 build-only
2 build-only
3 lint
4 build-only
5 scan
6 lint
7 build-only
8 build-only
9 lint
10 scan
11 build-only
12 lint
13 build-only
14 build-only
15 full-pipeline
```

**Example 2:**

```text
=== Capacity per environment ===
prod     servers=3 cpu=24  ram=80 GB [web-01, web-02, db-01]
staging  servers=1 cpu=2   ram=4  GB [web-01]
dev      servers=1 cpu=8   ram=16 GB [batch-01]

=== Violations ===
- prod/web-02      outdated OS ubuntu-20.04
- prod/web-02      high CPU 91%
- staging/web-01   missing owner tag
- dev/batch-01     outdated OS ubuntu-18.04

=== Summary ===
Servers: 5 | with issues: 3 | violations: 4
Compliance: 40%
```

## 8. Common Mistakes

**1. Coding before understanding**

Write the steps in plain English first. Most bugs are thinking bugs, not typing bugs.

**2. Not testing edge cases**

What if the inventory is empty? `len(inventory)` would be 0 and the percentage divides by zero. Guard with `if inventory:`.

**3. Counting violations instead of servers**

One server can break several rules. Use a set of names to count unique servers.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Prime numbers:** Print all prime numbers between 2 and 50 using nested loops and `for...else`.
- **Task 2 (Medium) — Second largest:** Find the second-largest unique value in `[45, 91, 23, 91, 78, 60]` without using `sort()`/`sorted()`.
- **Task 3 (Practical Challenge) — Extend the inventory report:** Using the mini-project inventory (copy it), add: (a) the busiest server per environment, (b) a list of owners with the number of servers each owns (empty owner shown as `UNASSIGNED`), and (c) a recommendation line: scale up any env where average CPU util > 50%.

## 10. DevOps/MLOps Connection

- **DevOps:** inventory audits, compliance reports (CIS benchmarks), and capacity reports are this exact pattern: load → group → check rules → summarise.
- **Cloud:** AWS Config rules and tag-compliance scripts work the same way on real boto3 data (Day 82, Project 5).
- **Data engineering:** group-and-aggregate is the foundation of SQL `GROUP BY` and Pandas `groupby` (Day 89).

## 11. Interview Questions

**Q1. How do you approach a new programming problem?**

<details><summary>Show answer</summary>

Clarify input and output, work through an example by hand, write steps in plain language, choose data structures, implement, test with edge cases.

</details>

**Q2. How would you find duplicates in a list efficiently?**

<details><summary>Show answer</summary>

Track seen items in a set; any item already in the set is a duplicate (O(n)).

</details>

**Q3. What data structure would you use to group records by a field?**

<details><summary>Show answer</summary>

A dict mapping the field value to a list of records (`setdefault` or `collections.defaultdict(list)`).

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 35 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 034](../../03-dictionaries-logic/day-034/README.md) | [📚 Phase 3: Dictionaries and Programming Logic](../README.md) | [🏠 Home](../../README.md) | [Day 036 ➡](../../04-functions/day-036/README.md)
