# Day 020 — String Formatting (f-strings)

[⬅ Day 019](../../02-strings-collections/day-019/README.md) | [📚 Phase 2: Strings and Collections](../README.md) | [🏠 Home](../../README.md) | [Day 021 ➡](../../02-strings-collections/day-021/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 2 — Strings and Collections | 🟢 Beginner | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Insert variables into text with f-strings
- Format numbers: decimals, thousands separators, percentages
- Align text into tidy columns

## 2. Topic Explanation

Joining strings with `+` and `str()` gets messy. **f-strings** (formatted string literals, Python 3.6+) are the modern way:

```python
name = "web-01"
cpu = 73.456
print(f"{name} CPU is {cpu:.1f}%")   # web-01 CPU is 73.5%
```

- Put `f` before the opening quote.
- Anything inside `{ }` is evaluated as Python code and converted to text.
- After a colon you can add a **format spec**:

| Spec | Meaning | Example → result |
|---|---|---|
| `:.2f` | 2 decimals | `3.14159` → `3.14` |
| `:,` | thousands separator | `1234567` → `1,234,567` |
| `:.1%` | percentage | `0.756` → `75.6%` |
| `:>10` | right-align in 10 chars | |
| `:<10` | left-align | |
| `:^10` | centre | |
| `:05d` | pad with zeros | `7` → `00007` |

`{variable=}` (Python 3.8+) prints both name and value — great for debugging.

## 3. Syntax

```python
f"text {expression} more text"
f"{value:.2f}"        # 2 decimals
f"{value:>10}"        # right-align width 10
f"{value=}"           # debug: name=value
```

| Part | Meaning |
|---|---|
| `f"..."` | Marks an f-string. |
| `{expression}` | Any Python expression, evaluated and inserted. |
| `:spec` | Optional format specification after a colon. |
| `{x=}` | Self-documenting expression for debugging. |

## 4. Example 1 — Basic Example: f-string basics

```python
name = "Asha"
day = 20
progress = day / 100

print(f"Hello {name}, today is day {day}.")
print(f"Progress: {progress:.0%}")
print(f"Pi to 3 decimals: {3.14159265:.3f}")
print(f"Big number: {1234567890:,}")
print(f"Ticket number: {42:05d}")
print(f"Next day: {day + 1}")
print(f"{name=}, {day=}")
```

## 5. Example 2 — Practical Example: A formatted server report table

```python
servers = [
    ("web-01", 23.5, 41.0, 1_048_576),
    ("web-02", 87.25, 92.3, 524_288),
    ("db-01", 55.0, 78.75, 8_388_608),
]

print(f"{'HOST':<8} {'CPU%':>7} {'MEM%':>7} {'DISK(KB)':>12} {'STATUS':^10}")
print("-" * 48)
for host, cpu, mem, disk_kb in servers:              # loops: Day 29
    status = "ALERT" if cpu > 80 or mem > 90 else "ok"
    print(f"{host:<8} {cpu:>7.1f} {mem:>7.1f} {disk_kb:>12,} {status:^10}")

total_disk_gb = sum(s[3] for s in servers) / 1024 / 1024
print("-" * 48)
print(f"Total disk: {total_disk_gb:.2f} GB")
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `{progress:.0%}` multiplies by 100 and adds `%` with zero decimals.
- `{1234567890:,}` inserts thousands separators.
- `{42:05d}` pads the integer to 5 digits with zeros.
- `{day + 1}` shows that any expression works inside braces.
- `{name=}` prints `name='Asha'` — handy debugging.

**Example 2**
- The header uses `<` (left) and `>` (right) alignment with fixed widths so columns line up.
- `{cpu:>7.1f}` = right-aligned, width 7, 1 decimal.
- `{disk_kb:>12,}` = width 12 with thousands separators.
- `{status:^10}` centres the status.

## 7. Expected Output

**Example 1:**

```text
Hello Asha, today is day 20.
Progress: 20%
Pi to 3 decimals: 3.142
Big number: 1,234,567,890
Ticket number: 00042
Next day: 21
name='Asha', day=20
```

**Example 2:**

```text
HOST        CPU%    MEM%     DISK(KB)   STATUS  
------------------------------------------------
web-01      23.5    41.0    1,048,576     ok    
web-02      87.2    92.3      524,288   ALERT   
db-01       55.0    78.8    8,388,608     ok    
------------------------------------------------
Total disk: 9.50 GB
```

## 8. Common Mistakes

**1. Forgetting the `f`**

`"Hello {name}"` prints the braces literally. Add `f` before the quote.

**2. Quote clashes**

`f"{data["key"]}"` fails on older Pythons. Use different quotes: `f"{data['key']}"`.

**3. Formatting text as a number**

`f"{'5':.2f}"` raises `ValueError`. Convert to `float` first.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Introduce a service:** With `service = "orders"`, `replicas = 3`, `version = "2.1.0"`, print `orders v2.1.0 running with 3 replicas` using one f-string.
- **Task 2 (Medium) — Format metrics:** Print `request_count = 1532874` with separators, `latency = 0.234567` seconds as milliseconds with 1 decimal, and `success_ratio = 0.98765` as a percentage with 2 decimals.
- **Task 3 (Practical Challenge) — Pod status table:** Given a list of pods `[("api-7d9f", "Running", 0, 12.3), ("worker-5c2a", "CrashLoopBackOff", 14, 0.0), ("redis-0", "Running", 1, 3.75)]` (name, status, restarts, age in hours), print an aligned table like `kubectl get pods` with columns NAME, STATUS, RESTARTS, AGE (age with 1 decimal + `h`).

## 10. DevOps/MLOps Connection

- **DevOps:** readable CLI output, log messages, Slack/Teams alert text, generated config files.
- **Cloud:** building resource names `f"{project}-{env}-bucket"` and ARNs.
- **MLOps:** logging metrics `f"accuracy={acc:.3f}"`, naming model artefacts `f"model-v{version}.joblib"`.

## 11. Interview Questions

**Q1. What are f-strings and why are they preferred?**

<details><summary>Show answer</summary>

String literals prefixed with `f` that embed expressions in `{}`. They are faster and more readable than `%` formatting or `str.format()`.

</details>

**Q2. How do you format a float to two decimal places?**

<details><summary>Show answer</summary>

`f"{value:.2f}"`.

</details>

**Q3. What does `f"{x=}"` print?**

<details><summary>Show answer</summary>

The expression text and its value, e.g. `x=42` — useful for debugging.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 20 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 019](../../02-strings-collections/day-019/README.md) | [📚 Phase 2: Strings and Collections](../README.md) | [🏠 Home](../../README.md) | [Day 021 ➡](../../02-strings-collections/day-021/README.md)
