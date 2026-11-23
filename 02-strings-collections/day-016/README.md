# Day 016 — Strings Introduction

[⬅ Day 015](../../01-python-fundamentals/day-015/README.md) | [📚 Phase 2: Strings and Collections](../README.md) | [🏠 Home](../../README.md) | [Day 017 ➡](../../02-strings-collections/day-017/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 2 — Strings and Collections | 🟢 Beginner | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Create strings with single, double and triple quotes
- Join (concatenate) and repeat strings
- Use `len()` and the `in` operator on strings
- Understand that strings are immutable

## 2. Topic Explanation

A **string** (`str`) is a sequence of characters — letters, digits, spaces, symbols. Hostnames, log lines, file paths, commands, JSON text: almost everything a DevOps engineer handles is a string.

Key facts:
- Create with `'single'`, `"double"` or `"""triple"""` quotes.
- `+` **concatenates** (joins): `"web" + "-01"` → `"web-01"`.
- `*` **repeats**: `"-" * 10`.
- `len(text)` returns the number of characters.
- `"err" in line` checks whether a substring exists — the Python version of `grep -q`.
- Strings are **immutable**: you cannot change a character in place. Operations always return a **new** string.

Analogy: a string is like a train of carriages, each carrying one character. You can look at any carriage or build a new train, but you cannot swap a carriage on the existing train.

## 3. Syntax

```python
text = "hello"
combined = text1 + text2
repeated = text * 3
length = len(text)
found = "sub" in text
```

| Part | Meaning |
|---|---|
| `+` | Joins two strings into a new one. |
| `*` | Repeats a string n times. |
| `len()` | Number of characters (spaces count too). |
| `in / not in` | Substring test that returns True/False. |

## 4. Example 1 — Basic Example: String basics

```python
first_name = "Ada"
last_name = 'Lovelace'
full_name = first_name + " " + last_name

print(full_name)
print("Length:", len(full_name))
print("Contains 'love'?", "love" in full_name)
print("Contains 'Love'?", "Love" in full_name)
print("=" * 20)

quote = "It's a \"great\" day"
print(quote)
```

## 5. Example 2 — Practical Example: Inspecting a log line

```python
log_line = "2026-11-20 10:15:32 ERROR [payment-api] Database connection timeout"

print("Line length:", len(log_line), "characters")

if "ERROR" in log_line:
    print("This is an error line")

if "timeout" in log_line:
    print("Root cause hint: something timed out")

if "WARNING" not in log_line:
    print("Not a warning")

service = "payment-api"
alert = "ALERT: " + service + " reported an error"
print(alert)
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `first_name + " " + last_name` joins three strings (including a space).
- `len()` counts all characters including the space: 12.
- `"love" in full_name` is False because the name contains `Love` with a capital L — matching is case-sensitive.
- `\"` lets you put double quotes inside a double-quoted string.

**Example 2**
- `"ERROR" in log_line` is the Python equivalent of `grep ERROR`.
- `not in` is the negative test.
- The alert message is built with `+`.

## 7. Expected Output

**Example 1:**

```text
Ada Lovelace
Length: 12
Contains 'love'? False
Contains 'Love'? True
====================
It's a "great" day
```

**Example 2:**

```text
Line length: 67 characters
This is an error line
Root cause hint: something timed out
Not a warning
ALERT: payment-api reported an error
```

## 8. Common Mistakes

**1. Trying to modify a character**

`name[0] = "a"` raises `TypeError: 'str' object does not support item assignment`. Create a new string instead.

**2. Joining a number with `+`**

`"Port " + 80` fails. Use `str(80)` or an f-string.

**3. Case-sensitive searches**

`"error" in "ERROR found"` is False. Normalise with `.lower()` (Day 19).

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Full hostname:** Given `service = "auth"`, `env = "prod"`, `number = "03"`, build the hostname `auth-prod-03` with `+` and print it with its length.
- **Task 2 (Medium) — Keyword scanner:** Given the log line `"2026-11-20 10:21:01 WARNING Disk usage 91% on /var"`, print which of the words ERROR, WARNING, Disk, disk are present.
- **Task 3 (Practical Challenge) — Banner generator:** Given a message `"Deployment v2.3.0 complete"`, print it framed in a box of `#` characters whose width automatically matches the message length + 4.

## 10. DevOps/MLOps Connection

- **DevOps:** log lines, command output, hostnames and file paths are all strings. `in` replaces many `grep` calls.
- **Cloud:** ARNs (`arn:aws:s3:::my-bucket`) and resource IDs are strings you build and inspect.
- **Data engineering:** raw data often arrives as text before parsing.
- **ML:** NLP models start from strings; even tabular ML has string columns (categories) to encode.

## 11. Interview Questions

**Q1. Are Python strings mutable?**

<details><summary>Show answer</summary>

No, they are immutable. Every modification returns a new string.

</details>

**Q2. How do you check if a substring exists in a string?**

<details><summary>Show answer</summary>

With the `in` operator: `"ERROR" in line`.

</details>

**Q3. What is the difference between `'...'` and `"..."`?**

<details><summary>Show answer</summary>

None — both create strings. Pick one style and use the other when the text contains that quote.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 16 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 015](../../01-python-fundamentals/day-015/README.md) | [📚 Phase 2: Strings and Collections](../README.md) | [🏠 Home](../../README.md) | [Day 017 ➡](../../02-strings-collections/day-017/README.md)
