# Day 021 — Lists

[⬅ Day 020](../../02-strings-collections/day-020/README.md) | [📚 Phase 2: Strings and Collections](../README.md) | [🏠 Home](../../README.md) | [Day 022 ➡](../../02-strings-collections/day-022/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 2 — Strings and Collections | 🟢 Beginner | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Create lists and understand that they are ordered and mutable
- Add, change and remove items
- Use `len()`, `in`, `sum()`, `min()`, `max()` and `sorted()` with lists

## 2. Topic Explanation

A **list** is an ordered collection of items inside square brackets:

```python
servers = ["web-01", "web-02", "db-01"]
```

- **Ordered:** items keep their position.
- **Mutable:** you can add, change and remove items after creation.
- **Mixed types allowed** (but usually you keep one kind per list).
- **Duplicates allowed.**

Analogy: a list is a shopping list — you can add things, cross things off, and the order you wrote them is kept.

Useful built-ins: `len(lst)`, `x in lst`, `sum(numbers)`, `min()`, `max()`, `sorted(lst)` (returns a new sorted list).

In Bash you would use arrays (`servers=(web-01 web-02)`); Python lists are far easier to work with.

## 3. Syntax

```python
my_list = [item1, item2, item3]
empty = []
my_list.append(item)     # add to end
my_list[0] = new_value   # change
my_list.remove(item)     # remove by value
```

| Part | Meaning |
|---|---|
| `[ ]` | Square brackets create a list. |
| `append(x)` | Adds x to the end. |
| `lst[i] = x` | Replaces the item at index i. |
| `remove(x)` | Removes the first occurrence of x. |
| `sorted(lst)` | Returns a new sorted list; the original is unchanged. |

## 4. Example 1 — Basic Example: Working with a list

```python
tools = ["git", "docker", "kubernetes"]
print(tools)
print("Count:", len(tools))

tools.append("terraform")
print("After append:", tools)

tools[0] = "github"
print("After change:", tools)

tools.remove("docker")
print("After remove:", tools)

print("Is kubernetes in the list?", "kubernetes" in tools)
print("Sorted copy:", sorted(tools))
print("Original order kept:", tools)
```

## 5. Example 2 — Practical Example: Response-time statistics

```python
response_times_ms = [120, 98, 250, 134, 87, 1500, 143, 110]

print("Samples:", len(response_times_ms))
print("Fastest:", min(response_times_ms), "ms")
print("Slowest:", max(response_times_ms), "ms")
average = sum(response_times_ms) / len(response_times_ms)
print(f"Average: {average:.1f} ms")

sorted_times = sorted(response_times_ms)
middle = len(sorted_times) // 2
median = (sorted_times[middle - 1] + sorted_times[middle]) / 2
print(f"Median: {median:.1f} ms  (less affected by the 1500 ms outlier)")

slow_requests = []
for t in response_times_ms:           # loops are covered on Day 29
    if t > 200:
        slow_requests.append(t)
print("Slow requests (>200 ms):", slow_requests)
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `append` adds to the end; `tools[0] = ...` replaces the first item; `remove` deletes by value.
- `sorted(tools)` returns a **new** list — `tools` keeps its order.

**Example 2**
- `min`, `max`, `sum`, `len` give quick statistics.
- The median needs a sorted list; with 8 values it is the average of the two middle values.
- Building `slow_requests` starts with an empty list and `append`s matching values — a pattern you will use constantly.

## 7. Expected Output

**Example 1:**

```text
['git', 'docker', 'kubernetes']
Count: 3
After append: ['git', 'docker', 'kubernetes', 'terraform']
After change: ['github', 'docker', 'kubernetes', 'terraform']
After remove: ['github', 'kubernetes', 'terraform']
Is kubernetes in the list? True
Sorted copy: ['github', 'kubernetes', 'terraform']
Original order kept: ['github', 'kubernetes', 'terraform']
```

**Example 2:**

```text
Samples: 8
Fastest: 87 ms
Slowest: 1500 ms
Average: 305.2 ms
Median: 127.0 ms  (less affected by the 1500 ms outlier)
Slow requests (>200 ms): [250, 1500]
```

## 8. Common Mistakes

**1. Removing a missing item**

`lst.remove("x")` raises `ValueError` if `x` is not there. Check with `in` first.

**2. `lst = lst.append(x)`**

`append` returns `None`, so this destroys your list. Just call `lst.append(x)`.

**3. Copying with `=`**

`b = a` does NOT copy; both names point to the same list. Use `a.copy()` or `a[:]`.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Team list:** Create a list of 3 team members, add 2 more, replace the second one, remove the last one and print the final list and its length.
- **Task 2 (Medium) — Port audit:** Given open ports `[22, 80, 443, 3306, 8080, 22]`, print how many there are, the highest port, whether 3306 (MySQL) is exposed and a sorted list without changing the original.
- **Task 3 (Practical Challenge) — Build durations report:** Given CI build durations in seconds `[312, 298, 1045, 305, 287, 330, 299]`, print min, max, average (1 decimal), and a list of builds slower than 1.5 × the average. Then remove those outliers into a new list and print the new average.

## 10. DevOps/MLOps Connection

- **DevOps:** lists of servers, ports, files, failed jobs, Docker images to clean up.
- **Cloud:** boto3 returns lists of instances, buckets, objects.
- **Data / ML:** a column of values, a batch of predictions, a list of feature names. NumPy arrays (Day 84) are the high-performance cousin of lists.

## 11. Interview Questions

**Q1. What is the difference between a list and a tuple?**

<details><summary>Show answer</summary>

Lists are mutable (can change); tuples are immutable.

</details>

**Q2. What is the difference between `sorted(lst)` and `lst.sort()`?**

<details><summary>Show answer</summary>

`sorted()` returns a new list; `.sort()` sorts in place and returns `None`.

</details>

**Q3. How do you copy a list correctly?**

<details><summary>Show answer</summary>

`lst.copy()`, `lst[:]` or `list(lst)` (shallow copy). For nested lists use `copy.deepcopy`.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 21 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 020](../../02-strings-collections/day-020/README.md) | [📚 Phase 2: Strings and Collections](../README.md) | [🏠 Home](../../README.md) | [Day 022 ➡](../../02-strings-collections/day-022/README.md)
