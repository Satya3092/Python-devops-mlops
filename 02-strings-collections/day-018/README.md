# Day 018 — String Slicing

[⬅ Day 017](../../02-strings-collections/day-017/README.md) | [📚 Phase 2: Strings and Collections](../README.md) | [🏠 Home](../../README.md) | [Day 019 ➡](../../02-strings-collections/day-019/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 2 — Strings and Collections | 🟢 Beginner | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Extract substrings with `text[start:stop]`
- Use the `step` value, including reversing with `[::-1]`
- Know that slicing never raises IndexError

## 2. Topic Explanation

**Slicing** extracts a part of a string: `text[start:stop:step]`.

- `start` — index where the slice begins (included). Default: beginning.
- `stop` — index where it ends (**excluded**). Default: end.
- `step` — how many characters to jump. Default: 1. Negative steps go backwards.

```
 text = "2026-11-20"
         0123456789
 text[0:4]  -> "2026"   (indexes 0,1,2,3)
 text[5:7]  -> "11"
 text[-2:]  -> "20"
```

Think of the indexes as **fence posts between characters**: the slice takes everything between two posts.

Out-of-range slices are safe: `"abc"[0:100]` simply returns `"abc"`.

## 3. Syntax

```python
text[start:stop]       # from start up to (not including) stop
text[:stop]            # from beginning
text[start:]           # to end
text[::step]           # every step-th character
text[::-1]             # reversed copy
```

| Part | Meaning |
|---|---|
| `start` | First index included (default 0). |
| `stop` | First index NOT included (default len). |
| `step` | Stride; negative means backwards. |
| `[:]` | Copy of the whole string. |

## 4. Example 1 — Basic Example: Slicing basics

```python
word = "automation"
print(word[0:4])     # auto
print(word[4:])      # mation
print(word[:4])      # auto
print(word[-4:])     # tion
print(word[::2])     # every second character
print(word[::-1])    # reversed
print(word[2:100])   # out of range is fine
```

## 5. Example 2 — Practical Example: Parsing a fixed-format log line

```python
log_line = "2026-11-20 10:15:32 ERROR Database connection timeout"

date = log_line[0:10]
time = log_line[11:19]
year = log_line[:4]
month = log_line[5:7]
hour = log_line[11:13]
rest = log_line[20:]

print("Date:", date)
print("Time:", time)
print("Year:", year, "| Month:", month, "| Hour:", hour)
print("Message part:", rest)

# Docker image reference: get the tag after the colon
image = "nginx:1.27-alpine"
colon_position = image.index(":")      # position of ':' (method from Day 19)
print("Image name:", image[:colon_position])
print("Image tag:", image[colon_position + 1:])
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `word[0:4]` takes indexes 0–3. `word[4:]` continues from 4 to the end, so `word[:4] + word[4:] == word`.
- `word[-4:]` takes the last four characters.
- `word[::-1]` uses step −1 to walk backwards → reversed string.

**Example 2**
- The log format is fixed: the date always occupies characters 0–9, the time 11–18. Slicing extracts them.
- `image.index(":")` finds the colon's position; slicing before/after it splits name and tag.

## 7. Expected Output

**Example 1:**

```text
auto
mation
auto
tion
atmto
noitamotua
tomation
```

**Example 2:**

```text
Date: 2026-11-20
Time: 10:15:32
Year: 2026 | Month: 11 | Hour: 10
Message part: ERROR Database connection timeout
Image name: nginx
Image tag: 1.27-alpine
```

## 8. Common Mistakes

**1. Forgetting stop is excluded**

`"2026-11-20"[0:3]` is `"202"`, not `"2026"`. Use `[0:4]`.

**2. Assuming fixed positions for variable data**

Slicing by position breaks if the format changes. For delimited data prefer `.split()` (Day 19).

**3. Confusing `[-1]` with `[-1:]`**

Both give the last character for strings, but `[-1]` fails on an empty string while `[-1:]` returns `""`.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Extract the extension:** Given `filename = "backup-2026-11-20.tar.gz"`, print the last 6 characters and the date part (characters 7–16).
- **Task 2 (Medium) — Palindrome check:** Check whether `"level"` and `"deploy"` are palindromes using slicing.
- **Task 3 (Practical Challenge) — Mask a secret:** Given an API key `"AKIAIOSFODNN7EXAMPLE"`, print it masked so only the first 4 and last 4 characters are visible, with `*` in between (same total length).

## 10. DevOps/MLOps Connection

- **DevOps:** extracting timestamps from logs, short Git SHAs (`commit[:7]`), masking secrets before printing them in CI logs.
- **Cloud:** trimming resource IDs, extracting account IDs from ARNs.
- **Data:** slicing date strings (`"2026-11-20"[:7]` → month) for grouping.

## 11. Interview Questions

**Q1. Is the stop index included in a slice?**

<details><summary>Show answer</summary>

No, the slice goes up to but not including `stop`.

</details>

**Q2. How do you reverse a string in Python?**

<details><summary>Show answer</summary>

`text[::-1]`.

</details>

**Q3. Does `s[5:100]` raise an error on a short string?**

<details><summary>Show answer</summary>

No, slicing clips out-of-range indexes silently.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 18 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 017](../../02-strings-collections/day-017/README.md) | [📚 Phase 2: Strings and Collections](../README.md) | [🏠 Home](../../README.md) | [Day 019 ➡](../../02-strings-collections/day-019/README.md)
