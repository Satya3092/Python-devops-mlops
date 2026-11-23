# Day 004 — Python Literals

[⬅ Day 003](../../01-python-fundamentals/day-003/README.md) | [📚 Phase 1: Python Fundamentals](../README.md) | [🏠 Home](../../README.md) | [Day 005 ➡](../../01-python-fundamentals/day-005/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 1 — Python Fundamentals | 🟢 Beginner | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Recognise numeric, string, boolean, None and collection literals
- Write integers in decimal, binary, octal and hexadecimal
- Use escape sequences, raw strings and multi-line strings

## 2. Topic Explanation

A **literal** is a fixed value written directly in your code. In `port = 8080`, the `8080` is an integer literal.

**Numeric literals**
- Integers: `42`, `-7`, `1_000_000` (underscores make big numbers readable).
- Binary `0b1010`, octal `0o755`, hexadecimal `0xFF`. Octal is how Linux file permissions are written — `chmod 755` is `0o755` in Python.
- Floats: `3.14`, `2.5e3` (scientific notation = 2500.0).

**String literals**
- Single `'text'` or double `"text"` quotes — same thing.
- Triple quotes `"""..."""` for multi-line text (great for templates).
- **Escape sequences** start with backslash: `\n` newline, `\t` tab, `\\` a real backslash, `\"` a quote.
- **Raw strings** `r"C:\new\folder"` turn off escapes — handy for Windows paths and regex.

**Other literals:** `True`, `False`, `None`, and collection literals `[ ]`, `( )`, `{ }`.

## 3. Syntax

```python
42  1_000_000  0b1010  0o755  0xFF      # int literals
3.14  2.5e3                             # float literals
'text'  "text"  """multi-line"""  r"raw\path"   # string literals
True  False  None                       # special literals
```

| Part | Meaning |
|---|---|
| `1_000_000` | Underscores are ignored; they only improve readability. |
| `0b / 0o / 0x` | Prefixes for binary, octal and hexadecimal integers. |
| `2.5e3` | Scientific notation: 2.5 × 10³. |
| `\n, \t` | Escape sequences for newline and tab inside strings. |
| `r"..."` | Raw string: backslashes are kept literally. |

## 4. Example 1 — Basic Example: Numbers in different bases

```python
million = 1_000_000
binary_value = 0b1010
file_mode = 0o755
max_byte = 0xFF
big_float = 2.5e3

print("million:", million)
print("0b1010 =", binary_value)
print("0o755 =", file_mode)
print("0xFF  =", max_byte)
print("2.5e3 =", big_float)
print("755 in octal back to text:", oct(file_mode))
```

## 5. Example 2 — Practical Example: Building a config file with string literals

```python
# Multi-line string - perfect for a config template
nginx_config = """server {
    listen 80;
    server_name example.com;
}"""
print(nginx_config)

# Escape sequences
print("Name:\tweb-01\nStatus:\tUP")
print("He said \"deploy now\"")

# Raw string keeps backslashes (Windows path)
windows_path = r"C:\new\tools\terraform.exe"
print(windows_path)
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `1_000_000` prints as `1000000`; underscores are only for humans.
- `0o755` is the octal number 755 = 493 in decimal. `oct()` converts it back to octal text.
- `2.5e3` is a float, so it prints as `2500.0`.

**Example 2**
- Triple quotes keep line breaks and indentation exactly as typed.
- `\t` inserts a tab and `\n` starts a new line inside a single string.
- `\"` lets you place a double quote inside a double-quoted string.
- With the `r` prefix, `\n` in `\new` is **not** turned into a newline.

## 7. Expected Output

**Example 1:**

```text
million: 1000000
0b1010 = 10
0o755 = 493
0xFF  = 255
2.5e3 = 2500.0
755 in octal back to text: 0o755
```

**Example 2:**

```text
server {
    listen 80;
    server_name example.com;
}
Name:	web-01
Status:	UP
He said "deploy now"
C:\new\tools\terraform.exe
```

## 8. Common Mistakes

**1. Windows paths without raw strings**

`"C:\new\temp"` contains `\n` and `\t`, which become a newline and a tab! Use `r"C:\new\temp"` or forward slashes.

**2. Writing permissions as `755`**

`os.chmod(path, 755)` sets the wrong permissions. You need the octal literal `0o755`.

**3. Leading zeros**

`port = 0080` is a `SyntaxError` in Python 3. Write `80`.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Readable numbers:** Store the number of requests per day `86400000` using underscores, the max file size 0xFFFF and permission 0o644. Print each value in decimal.
- **Task 2 (Medium) — Formatted report with escapes:** Print a small table using `\t` between columns and `\n` between rows for services nginx (80), postgres (5432) and redis (6379) — using a single `print()` call.
- **Task 3 (Practical Challenge) — Generate a Dockerfile:** Use a triple-quoted string to create the text of a simple Dockerfile (FROM python:3.12-slim, WORKDIR /app, COPY, RUN pip install, CMD). Print it, then print how many lines it has using `.count("\n") + 1`.

## 10. DevOps/MLOps Connection

- **DevOps / Linux:** File permissions are octal literals (`0o600` for SSH keys). Multi-line strings generate config files (nginx, systemd units, Dockerfiles).
- **Cloud automation:** User-data scripts for EC2 are usually triple-quoted strings inside Python.
- **Data engineering:** Raw strings are essential for regular expressions used to parse logs (Day 72).

## 11. Interview Questions

**Q1. What is a literal?**

<details><summary>Show answer</summary>

A value written directly in source code, such as `42`, `'web'`, `True` or `[1, 2]`.

</details>

**Q2. What does the `r` prefix do?**

<details><summary>Show answer</summary>

It creates a raw string where backslashes are not treated as escape characters. Common for regex and Windows paths.

</details>

**Q3. How do you write the Linux permission 750 in Python?**

<details><summary>Show answer</summary>

As an octal literal: `0o750`.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 4 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 003](../../01-python-fundamentals/day-003/README.md) | [📚 Phase 1: Python Fundamentals](../README.md) | [🏠 Home](../../README.md) | [Day 005 ➡](../../01-python-fundamentals/day-005/README.md)
