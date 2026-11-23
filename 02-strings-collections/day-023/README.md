# Day 023 — List Methods

[⬅ Day 022](../../02-strings-collections/day-022/README.md) | [📚 Phase 2: Strings and Collections](../README.md) | [🏠 Home](../../README.md) | [Day 024 ➡](../../02-strings-collections/day-024/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 2 — Strings and Collections | 🟢 Beginner | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Use `append`, `extend`, `insert`, `pop`, `remove`, `clear`
- Use `index`, `count`, `sort`, `reverse`, `copy`
- Know which methods change the list in place and return `None`

## 2. Topic Explanation

Lists come with methods that **change the list in place**:

| Method | Does |
|---|---|
| `append(x)` | Add one item at the end |
| `extend(iterable)` | Add many items at the end |
| `insert(i, x)` | Insert at position i |
| `pop(i=-1)` | Remove **and return** item (default: last) |
| `remove(x)` | Remove first matching value |
| `clear()` | Remove everything |
| `sort(reverse=False, key=None)` | Sort in place |
| `reverse()` | Reverse in place |
| `index(x)` | Position of first x |
| `count(x)` | How many times x appears |
| `copy()` | Shallow copy |

Most in-place methods return `None`. `pop()` is the exception — it returns the removed item, which makes it perfect for **stacks** (last in, first out) and **queues** (`pop(0)`, first in, first out).

`sort(key=...)` lets you sort by any rule, e.g. `key=len` sorts by length.

## 3. Syntax

```python
lst.append(x)          lst.extend([a, b])     lst.insert(i, x)
item = lst.pop()       lst.remove(x)          lst.clear()
lst.sort(reverse=True) lst.reverse()          lst.index(x)   lst.count(x)
```

| Part | Meaning |
|---|---|
| `append vs extend` | `append([1,2])` adds ONE item (a list); `extend([1,2])` adds two items. |
| `pop()` | Returns the removed item. |
| `sort(key=f)` | Sorts using the value returned by function f. |
| `reverse=True` | Sort descending. |

## 4. Example 1 — Basic Example: Exploring list methods

```python
queue = ["job-1", "job-2"]
queue.append("job-3")
queue.extend(["job-4", "job-5"])
queue.insert(0, "urgent-job")
print("Queue:", queue)

next_job = queue.pop(0)          # FIFO: take from the front
print("Processing:", next_job)
last_job = queue.pop()           # take from the end
print("Removed from end:", last_job)
print("Queue now:", queue)

print("Index of job-3:", queue.index("job-3"))
versions = [3, 1, 2, 3, 3]
print("Count of 3:", versions.count(3))
versions.sort()
print("Sorted:", versions)
versions.reverse()
print("Reversed:", versions)
```

## 5. Example 2 — Practical Example: Docker image cleanup planner

```python
images = ["app:1.0.3", "app:1.0.10", "app:1.0.1", "app:1.0.7", "app:1.0.9", "app:1.0.2"]
KEEP_LATEST = 3

def version_key(image):                    # functions are covered on Day 36
    version = image.split(":")[1]          # "1.0.10"
    return [int(part) for part in version.split(".")]

print("Text sort (wrong):", sorted(images))
images.sort(key=version_key, reverse=True)  # newest first, numeric order
print("Version sort:", images)

to_keep = images[:KEEP_LATEST]
to_delete = images[KEEP_LATEST:]
print("Keep:", to_keep)
print("Delete:", to_delete)

deleted = []
while to_delete:                            # while loops: Day 30
    image = to_delete.pop()
    deleted.append(image)
    print(f"docker rmi {image}")
print("Deleted", len(deleted), "images")
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `extend` adds each element of the given list; `insert(0, ...)` puts an item at the front.
- `pop(0)` removes the first item (queue behaviour); `pop()` removes the last (stack behaviour).
- `sort()` and `reverse()` change `versions` itself.

**Example 2**
- Sorting version strings as text puts `1.0.10` before `1.0.2` — wrong! A `key` function converts `"1.0.10"` to `[1, 0, 10]`, which sorts numerically.
- `reverse=True` puts the newest first, so slicing keeps the 3 latest.
- `while to_delete:` keeps popping until the list is empty.

## 7. Expected Output

**Example 1:**

```text
Queue: ['urgent-job', 'job-1', 'job-2', 'job-3', 'job-4', 'job-5']
Processing: urgent-job
Removed from end: job-5
Queue now: ['job-1', 'job-2', 'job-3', 'job-4']
Index of job-3: 2
Count of 3: 3
Sorted: [1, 2, 3, 3, 3]
Reversed: [3, 3, 3, 2, 1]
```

**Example 2:**

```text
Text sort (wrong): ['app:1.0.1', 'app:1.0.10', 'app:1.0.2', 'app:1.0.3', 'app:1.0.7', 'app:1.0.9']
Version sort: ['app:1.0.10', 'app:1.0.9', 'app:1.0.7', 'app:1.0.3', 'app:1.0.2', 'app:1.0.1']
Keep: ['app:1.0.10', 'app:1.0.9', 'app:1.0.7']
Delete: ['app:1.0.3', 'app:1.0.2', 'app:1.0.1']
docker rmi app:1.0.1
docker rmi app:1.0.2
docker rmi app:1.0.3
Deleted 3 images
```

## 8. Common Mistakes

**1. `append` instead of `extend`**

`a.append([4, 5])` gives `[1, 2, 3, [4, 5]]` (nested). Use `extend` to add items individually.

**2. `x = lst.sort()`**

`sort()` returns `None`. Use `sorted(lst)` if you need the result as a value.

**3. Sorting versions as strings**

`"1.10" < "1.9"` is True as text. Use a numeric key (or `packaging.version`).

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Stack of commands:** Use a list as a stack for an undo history: push `mkdir app`, `cd app`, `git init`, then pop twice and print what was undone and what remains.
- **Task 2 (Medium) — Merge and dedupe:** Merge `team_a = ["nginx", "redis"]` and `team_b = ["redis", "postgres", "nginx", "kafka"]` into one list with `extend`, count how many times `redis` appears, then build a sorted list without duplicates.
- **Task 3 (Practical Challenge) — Priority alert queue:** Alerts are tuples `(severity, message)` where 1 is most urgent: `[(3, "Disk 80%"), (1, "DB down"), (2, "High latency"), (1, "Payment API 500s"), (4, "Cert expires in 20 days")]`. Sort by severity, then process (pop from the front) only severity 1 and 2 alerts, printing each, and print what is left.

## 10. DevOps/MLOps Connection

- **DevOps:** job queues, retry queues, keeping the N newest artefacts/backups and deleting the rest (`sort` + slicing).
- **CI/CD:** collecting failed test names with `append`, merging results with `extend`.
- **MLOps:** keeping the top-k models sorted by a metric (`sort(key=..., reverse=True)`).

## 11. Interview Questions

**Q1. What is the difference between `append` and `extend`?**

<details><summary>Show answer</summary>

`append` adds its argument as a single element; `extend` iterates over its argument and adds each element.

</details>

**Q2. Which list method returns the removed element?**

<details><summary>Show answer</summary>

`pop()`.

</details>

**Q3. How would you implement a queue efficiently in Python?**

<details><summary>Show answer</summary>

Use `collections.deque` with `append` and `popleft` (O(1)); `list.pop(0)` is O(n).

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 23 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 022](../../02-strings-collections/day-022/README.md) | [📚 Phase 2: Strings and Collections](../README.md) | [🏠 Home](../../README.md) | [Day 024 ➡](../../02-strings-collections/day-024/README.md)
