# Day 025 — Sets and Set Operations

[⬅ Day 024](../../02-strings-collections/day-024/README.md) | [📚 Phase 2: Strings and Collections](../README.md) | [🏠 Home](../../README.md) | [Day 026 ➡](../../03-dictionaries-logic/day-026/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 2 — Strings and Collections | 🟢 Beginner | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Create sets and remove duplicates
- Use union, intersection, difference and symmetric difference
- Use sets for fast membership tests and comparisons

## 2. Topic Explanation

A **set** is an **unordered** collection of **unique** items:

```python
environments = {"dev", "staging", "prod", "dev"}   # -> {'dev', 'staging', 'prod'}
```

- Duplicates are removed automatically.
- No order and no indexing (`s[0]` is an error).
- Membership tests (`x in s`) are extremely fast, even with millions of items.
- An empty set is `set()` (because `{}` is an empty dict).

Set operations work like Venn diagrams:

| Operation | Operator | Method | Meaning |
|---|---|---|---|
| Union | `a \| b` | `a.union(b)` | in a OR b |
| Intersection | `a & b` | `a.intersection(b)` | in both |
| Difference | `a - b` | `a.difference(b)` | in a but not b |
| Symmetric difference | `a ^ b` | `a.symmetric_difference(b)` | in exactly one |

Add with `add(x)`, remove with `remove(x)` (error if missing) or `discard(x)` (no error).

Analogy: comparing two guest lists — who is on both, who is only on one.

## 3. Syntax

```python
my_set = {item1, item2}
empty = set()
unique = set(some_list)
a | b    a & b    a - b    a ^ b
my_set.add(x)    my_set.discard(x)
```

| Part | Meaning |
|---|---|
| `{ }` | Curly braces with values (not key: value) create a set. |
| `set(list)` | Converts any iterable to a set, removing duplicates. |
| `\| & - ^` | Union, intersection, difference, symmetric difference. |
| `issubset()` | `a <= b`: every item of a is in b. |

## 4. Example 1 — Basic Example: Set basics and operations

```python
visitors = ["10.0.0.1", "10.0.0.2", "10.0.0.1", "10.0.0.3", "10.0.0.2"]
unique_visitors = set(visitors)
print("Unique IPs:", sorted(unique_visitors))
print("Count:", len(unique_visitors))

a = {1, 2, 3, 4}
b = {3, 4, 5, 6}
print("Union:", a | b)
print("Intersection:", a & b)
print("a - b:", a - b)
print("Symmetric diff:", a ^ b)

a.add(10)
a.discard(99)          # no error even though 99 is missing
print("After add/discard:", sorted(a))
```

## 5. Example 2 — Practical Example: Configuration drift and access audit

```python
# Packages that SHOULD be installed (desired state) vs what IS installed
desired_packages = {"nginx", "git", "curl", "python3", "fail2ban"}
installed_packages = {"nginx", "git", "curl", "python3", "telnet", "ftp"}

missing = desired_packages - installed_packages
unexpected = installed_packages - desired_packages
compliant = desired_packages & installed_packages

print("Missing (install these):", sorted(missing))
print("Unexpected (remove these):", sorted(unexpected))
print("Compliant:", sorted(compliant))
print("Fully compliant?", desired_packages <= installed_packages)

# Who has access to production but is no longer on the team?
team_members = {"asha", "ravi", "john"}
prod_access = {"asha", "ravi", "john", "old_contractor", "intern2024"}
print("Revoke access for:", sorted(prod_access - team_members))
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `set(visitors)` removes duplicate IPs. We print `sorted()` because sets have no guaranteed order.
- The four operators show the Venn-diagram regions of `a` and `b`.
- `discard` silently ignores missing items; `remove` would raise `KeyError`.

**Example 2**
- This is the core idea of **configuration management** (Ansible, Puppet): compare *desired state* with *actual state*.
- `desired - installed` = what to install; `installed - desired` = what to remove.
- `desired <= installed` checks if desired is a subset (everything required is present).
- Access audits use the same difference operation.

## 7. Expected Output

**Example 1:**

```text
Unique IPs: ['10.0.0.1', '10.0.0.2', '10.0.0.3']
Count: 3
Union: {1, 2, 3, 4, 5, 6}
Intersection: {3, 4}
a - b: {1, 2}
Symmetric diff: {1, 2, 5, 6}
After add/discard: [1, 2, 3, 4, 10]
```

**Example 2:**

```text
Missing (install these): ['fail2ban']
Unexpected (remove these): ['ftp', 'telnet']
Compliant: ['curl', 'git', 'nginx', 'python3']
Fully compliant? False
Revoke access for: ['intern2024', 'old_contractor']
```

> ℹ️ Sets are unordered. When a set is printed directly (e.g. `{1, 2, 3}` operations above) the order on your machine may differ. Code that needs stable output uses `sorted()`.

## 8. Common Mistakes

**1. Creating an empty set with `{}`**

`{}` is a dict. Use `set()`.

**2. Indexing a set**

`s[0]` → `TypeError`. Convert to a list or sort it first.

**3. Adding mutable items**

`{[1, 2]}` fails — set items must be hashable. Use tuples instead of lists.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Remove duplicates:** Given `tags = ["web", "prod", "web", "api", "prod", "linux"]`, print the unique tags sorted and how many duplicates were removed.
- **Task 2 (Medium) — Skills gap:** Given `my_skills = {"linux", "git", "docker", "kubernetes", "aws"}` and `mlops_skills = {"python", "docker", "kubernetes", "mlflow", "aws", "fastapi"}`, print what you already have, what you need to learn, and all skills combined.
- **Task 3 (Practical Challenge) — Security group audit:** Allowed ports policy: `{22, 80, 443}`. Two servers have open ports `web-01: {22, 80, 443, 8080}` and `web-02: {80, 443}`. For each server print unauthorised open ports, missing required ports (443 and 80 must be open), and a final COMPLIANT/NON-COMPLIANT verdict. Also print ports open on both servers.

## 10. DevOps/MLOps Connection

- **DevOps:** desired vs actual state (configuration drift), comparing package lists between servers, finding new/removed files between deployments.
- **Security:** auditing open ports, IAM users with access who left the team.
- **Data engineering:** finding records present in one system but not the other.
- **ML:** vocabularies of unique words; checking that train and test sets do not overlap (data leakage!).

## 11. Interview Questions

**Q1. What are the key properties of a set?**

<details><summary>Show answer</summary>

Unordered, unique elements, mutable (but elements must be hashable), fast O(1) membership tests.

</details>

**Q2. How do you find items in list A that are not in list B?**

<details><summary>Show answer</summary>

`set(a) - set(b)`.

</details>

**Q3. What is the difference between `remove` and `discard`?**

<details><summary>Show answer</summary>

`remove` raises `KeyError` if the item is missing; `discard` does nothing.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 25 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 024](../../02-strings-collections/day-024/README.md) | [📚 Phase 2: Strings and Collections](../README.md) | [🏠 Home](../../README.md) | [Day 026 ➡](../../03-dictionaries-logic/day-026/README.md)
