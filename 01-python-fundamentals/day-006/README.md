# Day 006 — Type Conversion

[⬅ Day 005](../../01-python-fundamentals/day-005/README.md) | [📚 Phase 1: Python Fundamentals](../README.md) | [🏠 Home](../../README.md) | [Day 007 ➡](../../01-python-fundamentals/day-007/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 1 — Python Fundamentals | 🟢 Beginner | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Convert between `str`, `int`, `float` and `bool`
- Understand implicit vs explicit conversion
- Handle conversion of user input safely

## 2. Topic Explanation

**Type conversion** (also called *casting*) means changing a value from one type into another.

- **Implicit conversion:** Python does it for you when it is safe, e.g. `3 + 2.5` gives `5.5` (int is promoted to float).
- **Explicit conversion:** you ask for it with a function: `int()`, `float()`, `str()`, `bool()`, `list()`...

Common conversions:

| Call | Result |
|---|---|
| `int("42")` | `42` |
| `float("3.5")` | `3.5` |
| `int(3.99)` | `3` (cuts off the decimal, no rounding) |
| `str(8080)` | `"8080"` |
| `bool(0)`, `bool("")` | `False` |
| `bool(5)`, `bool("no")` | `True` (any non-empty text is True!) |

If the text cannot be converted — `int("abc")` — Python raises a `ValueError`. You will learn to catch these on Day 52.

Analogy: converting a type is like converting a document from `.docx` to `.pdf`. The content is the same idea but in a format that a particular tool understands.

## 3. Syntax

```python
int(value)     float(value)     str(value)     bool(value)
number = int(input("Enter a number: "))
```

| Part | Meaning |
|---|---|
| `int(x)` | Converts text or float to a whole number. |
| `float(x)` | Converts to a decimal number. |
| `str(x)` | Converts any value to text. |
| `bool(x)` | `False` for 0, 0.0, empty text/collections and None; otherwise `True`. |

## 4. Example 1 — Basic Example: Basic conversions

```python
port_text = "8080"
port_number = int(port_text)
print(port_number + 1)

price = float("19.99")
print(price * 2)

print(int(7.9))          # decimal part is cut off
print(round(7.9))        # round() rounds to nearest
print(str(443) + "/tcp")

print(bool(0), bool(1), bool(""), bool("False"))
print(3 + 2.5, type(3 + 2.5))   # implicit conversion to float
```

## 5. Example 2 — Practical Example: Disk usage calculator from user input

```python
total_gb = float(input("Total disk size (GB): "))
used_gb = float(input("Used space (GB): "))

free_gb = total_gb - used_gb
used_percent = used_gb / total_gb * 100

print("Free space:", free_gb, "GB")
print("Used:", round(used_percent, 1), "%")
print("Used (whole number):", int(used_percent), "%")
```

*This example asks for input. In the expected output below, the typed values appear after each prompt.*

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `int("8080")` turns text into a number so `+ 1` performs maths (`8081`), not text joining.
- `int(7.9)` truncates to `7`; `round(7.9)` rounds to `8`.
- `str(443) + "/tcp"` converts the number to text so it can be joined to another string.
- `bool("False")` is `True` — it is a non-empty string! Only empty text is falsy.

**Example 2**
- `float(input(...))` converts the typed text immediately into a decimal number.
- Percentage = used / total × 100. `round(x, 1)` keeps one decimal place.

## 7. Expected Output

**Example 1:**

```text
8081
39.98
7
8
443/tcp
False True False True
5.5 <class 'float'>
```

**Example 2:**

```text
Total disk size (GB): 500
Used space (GB): 412.5
Free space: 87.5 GB
Used: 82.5 %
Used (whole number): 82 %
```

## 8. Common Mistakes

**1. `int("3.5")` fails**

`int()` cannot read decimal text. Use `int(float("3.5"))` if you need a whole number.

**2. `bool("False")` is `True`**

To parse yes/no text, compare explicitly: `value.lower() in ("true", "yes", "1")`.

**3. Joining text and numbers with `+`**

`"Port: " + 80` raises `TypeError`. Use `"Port: " + str(80)` or an f-string (Day 20).

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Minutes to seconds:** Ask for a timeout in minutes (may be a decimal, e.g. 2.5) and print it in seconds as an integer.
- **Task 2 (Medium) — Environment flag parser:** Environment variables are always text. Given `debug_flag = "false"` and `workers = "4"`, convert them correctly to a bool and an int and print the types. Show why `bool("false")` would be wrong.
- **Task 3 (Practical Challenge) — Bandwidth estimator:** Ask for a file size in GB and a network speed in Mbps. Calculate the transfer time in minutes (1 GB = 8000 megabits). Print the result rounded to 2 decimals.

## 10. DevOps/MLOps Connection

- **DevOps:** Environment variables and CLI arguments are always strings. Converting `"3"` → `3` replicas or `"true"` → `True` is daily work.
- **Cloud automation:** AWS tags and many API values are strings; you convert them before comparing (e.g. cost thresholds).
- **Data engineering / ML:** CSV files load as text; columns must be converted to numbers before analysis or model training. Wrong conversions are a top source of data bugs.

## 11. Interview Questions

**Q1. What is the difference between implicit and explicit type conversion?**

<details><summary>Show answer</summary>

Implicit is automatic (int + float → float). Explicit is when you call a function such as `int()` or `str()`.

</details>

**Q2. What does `int(9.99)` return?**

<details><summary>Show answer</summary>

`9` — it truncates toward zero, it does not round.

</details>

**Q3. What happens with `int("ten")`?**

<details><summary>Show answer</summary>

Python raises `ValueError: invalid literal for int()`.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 6 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 005](../../01-python-fundamentals/day-005/README.md) | [📚 Phase 1: Python Fundamentals](../README.md) | [🏠 Home](../../README.md) | [Day 007 ➡](../../01-python-fundamentals/day-007/README.md)
