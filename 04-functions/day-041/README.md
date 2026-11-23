# Day 041 — Variable-Length Arguments (*args)

[⬅ Day 040](../../04-functions/day-040/README.md) | [📚 Phase 4: Functions and Modular Programming](../README.md) | [🏠 Home](../../README.md) | [Day 042 ➡](../../04-functions/day-042/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 4 — Functions and Modular Programming | 🟡 Beginner+ | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Accept any number of positional arguments with `*args`
- Loop over `args` inside the function
- Unpack a list into arguments with `*` at call time

## 2. Topic Explanation

Sometimes you don't know how many values a caller will pass. `*args` collects **all extra positional arguments into a tuple**:

```python
def total(*numbers):
    return sum(numbers)

total(1, 2)          # numbers = (1, 2)
total(5, 10, 15, 20) # numbers = (5, 10, 15, 20)
```

- The `*` is what matters; `args` is just the conventional name.
- `*args` comes after normal parameters: `def ping(timeout, *hosts):`.
- Built-ins like `print(*objects)` and `max(*values)` use this.

The `*` also works the other way, at **call** time, to **unpack** a list/tuple into separate arguments:
```python
servers = ["web-01", "web-02"]
ping(5, *servers)     # same as ping(5, "web-01", "web-02")
```

Analogy: `*args` is an expandable bag — the function accepts whatever number of items you put in it.

## 3. Syntax

```python
def function_name(fixed_param, *args):
    for value in args:
        ...

function_name(1, 2, 3, 4)
function_name(1, *my_list)       # unpack at call time
```

| Part | Meaning |
|---|---|
| `*args` | Collects extra positional arguments into a tuple. |
| `fixed params first` | Normal parameters come before `*args`. |
| `*my_list (in a call)` | Spreads a list into separate positional arguments. |

## 4. Example 1 — Basic Example: Summing any number of values

```python
def total(*numbers):
    print("Received:", numbers, type(numbers).__name__)
    return sum(numbers)


print(total(1, 2))
print(total(5, 10, 15, 20))
print(total())

values = [3, 6, 9]
print(total(*values))        # unpack the list

first, *middle, last = [1, 2, 3, 4, 5]
print(first, middle, last)
```

## 5. Example 2 — Practical Example: Running a command on many hosts

```python
def run_on_hosts(command, *hosts, user="ubuntu"):
    """Simulate running a command on any number of hosts."""
    if not hosts:
        print("No hosts given - nothing to do")
        return []
    results = []
    for host in hosts:
        print(f"ssh {user}@{host} '{command}'")
        results.append((host, "ok"))
    return results


run_on_hosts("uptime")
run_on_hosts("df -h /", "web-01", "web-02")

web_tier = ["web-01", "web-02", "web-03"]
db_tier = ["db-01"]
results = run_on_hosts("sudo systemctl restart node_exporter", *web_tier, *db_tier, user="admin")
print("Results:", results)


def merge_tags(*tag_lists):
    """Merge any number of tag lists into one sorted unique list."""
    merged = set()
    for tags in tag_lists:
        merged.update(tags)
    return sorted(merged)


print(merge_tags(["web", "prod"], ["prod", "linux"], ["monitoring"]))
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `numbers` is a tuple inside the function. With no arguments it is an empty tuple and `sum(())` is 0.
- `total(*values)` unpacks the list into three arguments.
- `first, *middle, last` shows the related "star unpacking" in assignments.

**Example 2**
- `command` is required; `*hosts` collects any number of hosts; `user` comes after `*hosts`, so it is automatically keyword-only.
- `*web_tier, *db_tier` spreads two lists into one call.
- `merge_tags(*tag_lists)` accepts any number of lists and merges them with a set.

## 7. Expected Output

**Example 1:**

```text
Received: (1, 2) tuple
3
Received: (5, 10, 15, 20) tuple
50
Received: () tuple
0
Received: (3, 6, 9) tuple
18
1 [2, 3, 4] 5
```

**Example 2:**

```text
No hosts given - nothing to do
ssh ubuntu@web-01 'df -h /'
ssh ubuntu@web-02 'df -h /'
ssh admin@web-01 'sudo systemctl restart node_exporter'
ssh admin@web-02 'sudo systemctl restart node_exporter'
ssh admin@web-03 'sudo systemctl restart node_exporter'
ssh admin@db-01 'sudo systemctl restart node_exporter'
Results: [('web-01', 'ok'), ('web-02', 'ok'), ('web-03', 'ok'), ('db-01', 'ok')]
['linux', 'monitoring', 'prod', 'web']
```

## 8. Common Mistakes

**1. Passing a list without `*`**

`total([1, 2, 3])` makes `numbers = ([1, 2, 3],)` — one argument, a list. `sum` then fails. Use `total(*[1, 2, 3])`.

**2. Trying to modify `args`**

`args` is a tuple, so `args.append()` fails. Convert with `list(args)`.

**3. Overusing `*args`**

If a function always needs exactly three values, name three parameters — it is clearer.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Average of any numbers:** Write `average(*values)` that returns the average, or `None` if no values were given. Test with (4, 8, 15), (10,), and no values.
- **Task 2 (Medium) — Build a path:** Write `build_path(*parts)` that joins any number of parts with `/` and makes sure the result starts with exactly one `/` (strip extra slashes from parts).
- **Task 3 (Practical Challenge) — Multi-service health summary:** Write `health_summary(title, *statuses)` where each status is a tuple `(service, code)`. Print a titled table, count healthy (2xx) vs unhealthy, and return the list of unhealthy services. Call it with 5 services, unpacking a list.

## 10. DevOps/MLOps Connection

- **DevOps:** helpers that accept any number of hosts, files or tags (`ansible`-style host lists, `rm file1 file2 ...`).
- **Logging:** Python's `logging.info("msg %s %s", a, b)` uses `*args`.
- **ML:** `np.concatenate`, `zip(*rows)` (transposing data) and many library functions rely on star-unpacking.

## 11. Interview Questions

**Q1. What type is `args` inside a function defined with `*args`?**

<details><summary>Show answer</summary>

A tuple.

</details>

**Q2. What does `*` do in a function call like `f(*items)`?**

<details><summary>Show answer</summary>

Unpacks the iterable into separate positional arguments.

</details>

**Q3. What happens to parameters declared after `*args`?**

<details><summary>Show answer</summary>

They become keyword-only.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 41 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 040](../../04-functions/day-040/README.md) | [📚 Phase 4: Functions and Modular Programming](../README.md) | [🏠 Home](../../README.md) | [Day 042 ➡](../../04-functions/day-042/README.md)
