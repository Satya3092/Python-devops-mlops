# Day 022 — List Indexing and Slicing

[⬅ Day 021](../../02-strings-collections/day-021/README.md) | [📚 Phase 2: Strings and Collections](../README.md) | [🏠 Home](../../README.md) | [Day 023 ➡](../../02-strings-collections/day-023/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 2 — Strings and Collections | 🟢 Beginner | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Access list items by positive and negative index
- Slice lists to get sub-lists
- Modify parts of a list with slice assignment and `del`

## 2. Topic Explanation

Lists use **exactly the same indexing and slicing rules** as strings (Days 17–18):

- `lst[0]` first item, `lst[-1]` last item.
- `lst[start:stop:step]` returns a **new list**.
- `lst[::-1]` reversed copy.

Because lists are **mutable**, you can also *assign* to indexes and slices:

```python
nodes[1] = "node-b"            # replace one item
nodes[1:3] = ["x", "y", "z"]   # replace a range (sizes can differ)
del nodes[0]                   # delete by index
```

Common patterns:
- `latest = items[-5:]` — last 5 items (like `tail -5`).
- `first_page = items[:10]` — first 10 (pagination, like `head`).
- `batches` — process big lists in chunks with slicing in a loop.

## 3. Syntax

```python
item = lst[index]
sub_list = lst[start:stop:step]
lst[index] = value
lst[start:stop] = [new, values]
del lst[index]
```

| Part | Meaning |
|---|---|
| `lst[i]` | Single item (IndexError if out of range). |
| `lst[a:b]` | New list with items a..b-1. |
| `lst[a:b] = [...]` | Slice assignment replaces a range. |
| `del lst[i]` | Deletes the item at index i. |

## 4. Example 1 — Basic Example: Indexing and slicing a list

```python
regions = ["us-east-1", "us-west-2", "eu-west-1", "ap-south-1", "ap-northeast-1"]
print("First:", regions[0])
print("Last:", regions[-1])
print("First two:", regions[:2])
print("Last two:", regions[-2:])
print("Every other:", regions[::2])
print("Reversed:", regions[::-1])

regions[1] = "us-west-1"
del regions[2]
print("Modified:", regions)
```

## 5. Example 2 — Practical Example: Tail of a log and batch processing

```python
log_lines = [f"line {n}: request served" for n in range(1, 13)]   # 12 fake lines

# Like 'tail -3'
print("Last 3 lines:")
for line in log_lines[-3:]:
    print("  ", line)

# Process hosts in batches of 4 (rolling deployment!)
hosts = [f"web-{n:02d}" for n in range(1, 11)]
batch_size = 4
for start in range(0, len(hosts), batch_size):
    batch = hosts[start:start + batch_size]
    print(f"Deploying batch starting at {start}: {batch}")

# Canary: deploy to the first host only, rest later
canary, remaining = hosts[0], hosts[1:]
print("Canary:", canary, "| remaining:", len(remaining))
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- Same index rules as strings. `regions[::2]` takes items 0, 2, 4.
- `regions[1] = ...` replaces; `del regions[2]` removes `eu-west-1`.

**Example 2**
- `log_lines[-3:]` is the Python equivalent of `tail -3`.
- `range(0, len(hosts), batch_size)` gives 0, 4, 8; slicing `hosts[start:start + 4]` gives each batch. The last batch is shorter — slicing handles that safely.
- `hosts[0]` and `hosts[1:]` split a canary from the rest.

## 7. Expected Output

**Example 1:**

```text
First: us-east-1
Last: ap-northeast-1
First two: ['us-east-1', 'us-west-2']
Last two: ['ap-south-1', 'ap-northeast-1']
Every other: ['us-east-1', 'eu-west-1', 'ap-northeast-1']
Reversed: ['ap-northeast-1', 'ap-south-1', 'eu-west-1', 'us-west-2', 'us-east-1']
Modified: ['us-east-1', 'us-west-1', 'ap-south-1', 'ap-northeast-1']
```

**Example 2:**

```text
Last 3 lines:
   line 10: request served
   line 11: request served
   line 12: request served
Deploying batch starting at 0: ['web-01', 'web-02', 'web-03', 'web-04']
Deploying batch starting at 4: ['web-05', 'web-06', 'web-07', 'web-08']
Deploying batch starting at 8: ['web-09', 'web-10']
Canary: web-01 | remaining: 9
```

## 8. Common Mistakes

**1. Expecting a slice to be a single item**

`hosts[0:1]` is a list `['web-01']`, not the string `'web-01'`.

**2. Index errors on empty lists**

`[][0]` raises `IndexError`. Check `if lst:` first.

**3. Modifying a list while looping over it**

Removing items inside `for x in lst` skips elements. Loop over a copy `lst[:]` or build a new list.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Head and tail:** Given `numbers = list(range(1, 21))`, print the first 5, the last 5 and the middle 10 items.
- **Task 2 (Medium) — Replace a range:** Given `stages = ["build", "test", "deploy-dev", "deploy-prod"]`, insert `security-scan` and `integration-test` instead of `test` using slice assignment, then delete `deploy-dev`.
- **Task 3 (Practical Challenge) — Rolling restart planner:** Given 11 pod names `pod-1`…`pod-11`, plan a rolling restart where at most 25 % of pods (rounded down, minimum 1) restart at once. Print each wave and the total number of waves.

## 10. DevOps/MLOps Connection

- **DevOps:** rolling deployments in batches (exactly how Ansible `serial:` and Kubernetes `maxUnavailable` behave), canary releases, tailing logs.
- **Cloud:** AWS APIs often accept at most N items per call — you send them in slices.
- **ML:** mini-batches for training and train/test splits are slices of data.

## 11. Interview Questions

**Q1. What does `lst[-3:]` return?**

<details><summary>Show answer</summary>

A new list with the last three items.

</details>

**Q2. How do you delete an item by index?**

<details><summary>Show answer</summary>

`del lst[i]` or `lst.pop(i)` (which also returns it).

</details>

**Q3. Is a slice of a list a copy or a view?**

<details><summary>Show answer</summary>

A new (shallow) copy.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 22 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 021](../../02-strings-collections/day-021/README.md) | [📚 Phase 2: Strings and Collections](../README.md) | [🏠 Home](../../README.md) | [Day 023 ➡](../../02-strings-collections/day-023/README.md)
