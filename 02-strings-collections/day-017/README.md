# Day 017 — String Indexing

[⬅ Day 016](../../02-strings-collections/day-016/README.md) | [📚 Phase 2: Strings and Collections](../README.md) | [🏠 Home](../../README.md) | [Day 018 ➡](../../02-strings-collections/day-018/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 2 — Strings and Collections | 🟢 Beginner | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Access individual characters using positive indexes
- Use negative indexes to read from the end
- Avoid `IndexError`

## 2. Topic Explanation

Every character in a string has a position number called an **index**. Python counts from **0**.

```
 text:   n  g  i  n  x
 index:  0  1  2  3  4
 neg:   -5 -4 -3 -2 -1
```

- `text[0]` → first character `"n"`.
- `text[-1]` → last character `"x"` (negative indexes count from the end).
- `text[len(text) - 1]` is the same as `text[-1]`.
- Asking for a position that does not exist → `IndexError: string index out of range`.

Analogy: indexes are like seat numbers in a cinema row that starts at seat 0. Negative indexes are like counting from the other aisle.

## 3. Syntax

```python
character = text[index]      # 0 = first
last = text[-1]              # -1 = last
```

| Part | Meaning |
|---|---|
| `text[0]` | First character. |
| `text[i]` | Character at position i (0-based). |
| `text[-1]` | Last character; `-2` is second to last. |
| `len(text) - 1` | Highest valid positive index. |

## 4. Example 1 — Basic Example: Reading characters by position

```python
tool = "kubernetes"
print("First:", tool[0])
print("Second:", tool[1])
print("Last:", tool[-1])
print("Second last:", tool[-2])
print("Length:", len(tool), "-> last index is", len(tool) - 1)
print("Same last char:", tool[len(tool) - 1])
```

## 5. Example 2 — Practical Example: Decoding instance naming conventions

```python
# Naming convention: <env-letter><region-digit>-<role>
# e.g. "p1-web" = production, region 1, web server
instance_name = "p1-web"

env_code = instance_name[0]
region_code = instance_name[1]
last_char = instance_name[-1]

if env_code == "p":
    environment = "production"
elif env_code == "s":
    environment = "staging"
else:
    environment = "development"

print("Instance:", instance_name)
print("Environment:", environment)
print("Region number:", region_code)
print("Ends with:", last_char)

# File permission string from 'ls -l'
permissions = "-rwxr-x---"
print("Is a directory?", permissions[0] == "d")
print("Owner can execute?", permissions[3] == "x")
print("Others can read?", permissions[7] == "r")
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- Index `0` is the first character, `-1` the last.
- `len(tool) - 1` computes the last valid index (9 for a 10-character word).

**Example 2**
- Fixed-position naming conventions can be decoded by index: position 0 holds the environment letter.
- In `ls -l` permission strings, position 0 is the file type, 1–3 owner, 4–6 group, 7–9 others. So `[3]` is the owner execute bit, `[7]` the others read bit.

## 7. Expected Output

**Example 1:**

```text
First: k
Second: u
Last: s
Second last: e
Length: 10 -> last index is 9
Same last char: s
```

**Example 2:**

```text
Instance: p1-web
Environment: production
Region number: 1
Ends with: b
Is a directory? False
Owner can execute? True
Others can read? False
```

## 8. Common Mistakes

**1. Starting to count from 1**

The first character is `text[0]`, not `text[1]`.

**2. Index out of range**

`"abc"[3]` raises `IndexError`. The last valid index is `len - 1`.

**3. Indexing an empty string**

`""[0]` fails. Check `if text:` first.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — First and last:** Given `region = "ap-south-1"`, print the first character, the last character and the character at index 3.
- **Task 2 (Medium) — Initials:** Given `first = "Linus"` and `last = "Torvalds"`, print the initials `L.T.` using indexing.
- **Task 3 (Practical Challenge) — Permission decoder:** Given `perm = "drwxr-xr--"`, print whether it is a directory, and for owner/group/others whether they can read, write and execute (use indexes 1–9).

## 10. DevOps/MLOps Connection

- **Linux/DevOps:** decoding permission strings, fixed-width command output, or naming conventions.
- **Data engineering:** fixed-width file formats (old mainframe exports) are parsed by position.
- **ML:** character-level text features start with indexing.

## 11. Interview Questions

**Q1. What index does the first character have?**

<details><summary>Show answer</summary>

0.

</details>

**Q2. What does `s[-1]` return?**

<details><summary>Show answer</summary>

The last character of the string.

</details>

**Q3. What error do you get for `s[100]` on a short string?**

<details><summary>Show answer</summary>

`IndexError: string index out of range`.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 17 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 016](../../02-strings-collections/day-016/README.md) | [📚 Phase 2: Strings and Collections](../README.md) | [🏠 Home](../../README.md) | [Day 018 ➡](../../02-strings-collections/day-018/README.md)
