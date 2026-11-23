# Day 033 — Nested Loops

[⬅ Day 032](../../03-dictionaries-logic/day-032/README.md) | [📚 Phase 3: Dictionaries and Programming Logic](../README.md) | [🏠 Home](../../README.md) | [Day 034 ➡](../../03-dictionaries-logic/day-034/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 3 — Dictionaries and Programming Logic | 🟢 Beginner | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Write loops inside loops
- Process 2-D data (tables, matrices)
- Generate combinations and understand the cost of nested loops

## 2. Topic Explanation

A **nested loop** is a loop inside another loop. For **every** iteration of the outer loop, the inner loop runs **completely**.

```python
for env in ["dev", "prod"]:          # outer: 2 times
    for service in ["api", "web"]:   # inner: 2 times per env
        print(env, service)          # runs 2 × 2 = 4 times
```

Analogy: a clock — the minute hand (inner loop) goes all the way around for every single step of the hour hand (outer loop).

Uses: tables/matrices, combinations (every environment × every region), comparing every item with every other item.

Watch the cost: 1,000 × 1,000 = 1,000,000 iterations. For big data, sets/dicts or Pandas are much faster.

## 3. Syntax

```python
for outer_item in outer_collection:
    for inner_item in inner_collection:
        do_something(outer_item, inner_item)
```

| Part | Meaning |
|---|---|
| `outer loop` | Runs once per outer item. |
| `inner loop` | Runs fully for each outer iteration. |
| `indentation` | The inner loop body is indented two levels. |
| `break` | Only exits the inner loop. |

## 4. Example 1 — Basic Example: Multiplication grid

```python
for row in range(1, 4):
    line = ""
    for col in range(1, 6):
        line += f"{row * col:4}"
    print(line)

pattern_rows = 4
for i in range(1, pattern_rows + 1):
    stars = ""
    for _ in range(i):
        stars += "*"
    print(stars)
```

## 5. Example 2 — Practical Example: Deployment matrix and duplicate detection

```python
environments = ["dev", "staging", "prod"]
regions = ["us-east-1", "eu-west-1"]
services = ["api", "worker"]

count = 0
for env in environments:
    for region in regions:
        for service in services:
            count += 1
            print(f"{count:2}. deploy {service:<7} -> {env:<8} @ {region}")
print("Total deployments:", count)

# Find servers that share the same IP (configuration error)
servers = [("web-01", "10.0.0.5"), ("web-02", "10.0.0.6"), ("db-01", "10.0.0.5")]
for i in range(len(servers)):
    for j in range(i + 1, len(servers)):          # compare each pair once
        if servers[i][1] == servers[j][1]:
            print(f"IP conflict: {servers[i][0]} and {servers[j][0]} both use {servers[i][1]}")
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- The inner loop builds one row; `{row * col:4}` right-aligns each product in 4 characters.
- The triangle pattern's inner loop runs `i` times, so each row has one more star.

**Example 2**
- Three nested loops produce every combination: 3 × 2 × 2 = 12 deployments (Ansible/Jenkins matrix builds work exactly like this).
- The pair comparison starts the inner loop at `i + 1` so each pair is compared once and a server is never compared with itself.

## 7. Expected Output

**Example 1:**

```text
   1   2   3   4   5
   2   4   6   8  10
   3   6   9  12  15
*
**
***
****
```

**Example 2:**

```text
 1. deploy api     -> dev      @ us-east-1
 2. deploy worker  -> dev      @ us-east-1
 3. deploy api     -> dev      @ eu-west-1
 4. deploy worker  -> dev      @ eu-west-1
 5. deploy api     -> staging  @ us-east-1
 6. deploy worker  -> staging  @ us-east-1
 7. deploy api     -> staging  @ eu-west-1
 8. deploy worker  -> staging  @ eu-west-1
 9. deploy api     -> prod     @ us-east-1
10. deploy worker  -> prod     @ us-east-1
11. deploy api     -> prod     @ eu-west-1
12. deploy worker  -> prod     @ eu-west-1
Total deployments: 12
IP conflict: web-01 and db-01 both use 10.0.0.5
```

## 8. Common Mistakes

**1. Wrong indentation level**

Putting a statement at the wrong level changes how many times it runs. Read the indentation carefully.

**2. Reusing the same loop variable**

`for i ...: for i ...:` overwrites the outer `i`. Use different names (`row`, `col`).

**3. Accidental O(n²)**

Checking `if x in big_list` inside a loop is a hidden nested loop. Convert `big_list` to a set.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Number pyramid:** Print a pyramid where row n contains the numbers 1..n separated by spaces, for 5 rows.
- **Task 2 (Medium) — Inventory per environment:** Given `inventory = {"dev": ["web-01"], "staging": ["web-01", "web-02"], "prod": ["web-01", "web-02", "web-03", "db-01"]}`, print every host as `<env>/<host>` and the host count per environment.
- **Task 3 (Practical Challenge) — Port scan matrix (simulated):** Given hosts `["10.0.0.1", "10.0.0.2", "10.0.0.3"]`, ports `[22, 80, 443, 3306]` and a simulated set of open `(host, port)` pairs `{("10.0.0.1", 22), ("10.0.0.1", 80), ("10.0.0.2", 443), ("10.0.0.3", 3306), ("10.0.0.3", 22)}`, print a table with OPEN/closed per host and port, then list hosts exposing MySQL.

## 10. DevOps/MLOps Connection

- **CI/CD:** matrix builds (Python versions × operating systems) — GitHub Actions `strategy.matrix` is a nested loop.
- **DevOps:** deploy every service to every region; check every port on every host.
- **Data/ML:** looping over rows and columns, or over hyper-parameter grids (`for lr in ...: for depth in ...:` — the idea behind `GridSearchCV`).

## 11. Interview Questions

**Q1. How many times does the inner body run for loops of size n and m?**

<details><summary>Show answer</summary>

n × m times.

</details>

**Q2. How do you break out of two nested loops at once?**

<details><summary>Show answer</summary>

Use a flag checked by the outer loop, put the loops in a function and `return`, or use `for...else` tricks.

</details>

**Q3. How can you avoid an O(n²) membership check?**

<details><summary>Show answer</summary>

Convert the inner collection to a set or dict for O(1) lookups.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 33 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 032](../../03-dictionaries-logic/day-032/README.md) | [📚 Phase 3: Dictionaries and Programming Logic](../README.md) | [🏠 Home](../../README.md) | [Day 034 ➡](../../03-dictionaries-logic/day-034/README.md)
