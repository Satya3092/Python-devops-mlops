# Day 019 — String Methods

[⬅ Day 018](../../02-strings-collections/day-018/README.md) | [📚 Phase 2: Strings and Collections](../README.md) | [🏠 Home](../../README.md) | [Day 020 ➡](../../02-strings-collections/day-020/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 2 — Strings and Collections | 🟢 Beginner | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Use the most important string methods: `strip`, `lower/upper`, `replace`, `split`, `join`
- Search with `startswith`, `endswith`, `find`, `count`
- Chain methods to clean messy text

## 2. Topic Explanation

A **method** is a function that belongs to a value. You call it with a dot: `text.upper()`. Since strings are immutable, methods **return a new string** — you must store or print the result.

The DevOps top-12:

| Method | Does | Example |
|---|---|---|
| `strip()` | Remove surrounding spaces/newlines | `" web \n".strip()` → `"web"` |
| `lower()` / `upper()` | Change case | `"PROD".lower()` |
| `replace(a, b)` | Replace text | `"v1".replace("1","2")` |
| `split(sep)` | Break into a **list** | `"a,b".split(",")` → `["a","b"]` |
| `sep.join(list)` | Join a list into text | `",".join(["a","b"])` |
| `startswith()` / `endswith()` | Prefix/suffix test | `f.endswith(".log")` |
| `find(x)` | Position of x or -1 | `"abc".find("c")` → 2 |
| `count(x)` | Occurrences | `"a-b-c".count("-")` |
| `isdigit()` | Only digits? | `"8080".isdigit()` |
| `title()` | Capitalise words | `"web server".title()` |

`split()` with no argument splits on any whitespace and ignores repeated spaces — perfect for command output like `df -h`.

## 3. Syntax

```python
new_text = text.method(arguments)
parts = text.split(",")
joined = "-".join(parts)
clean = text.strip().lower()     # chaining
```

| Part | Meaning |
|---|---|
| `.method()` | Calls a method on the string; returns a new value. |
| `split(sep)` | Returns a list of pieces. |
| `sep.join(items)` | The separator comes first, then the list. |
| `chaining` | Each method works on the result of the previous one. |

## 4. Example 1 — Basic Example: Everyday string methods

```python
raw = "   Production-Server  \n"
print(repr(raw))
clean = raw.strip()
print(repr(clean))
print(clean.lower())
print(clean.upper())
print(clean.replace("Server", "DB"))
print(clean.startswith("Prod"), clean.endswith(".log"))
print("Position of '-':", clean.find("-"))
print("Count of 'o':", clean.count("o"))
print("8080".isdigit(), "80a".isdigit())
```

## 5. Example 2 — Practical Example: Parsing command output and environment data

```python
# Output of 'df -h' for one filesystem
df_line = "/dev/sda1        50G   41G  9.0G  82% /"
fields = df_line.split()
print("Fields:", fields)
filesystem, size, used, available, use_percent, mount = fields
print("Mount", mount, "is", use_percent, "full")
usage = int(use_percent.rstrip("%"))
if usage > 80:
    print("Warning: high disk usage on", filesystem)

# Comma-separated host list from an environment variable
hosts_env = " web-01, web-02 ,web-03 "
hosts = [h.strip() for h in hosts_env.split(",")]   # list comprehension, Day 34
print("Hosts:", hosts)
print("Ansible inventory line:", " ".join(hosts))

# Normalise user input
answer = "  YES "
print("Confirmed?", answer.strip().lower() == "yes")

# Build a Kubernetes-style label from a title
title = "Payment Service API"
print("Label:", title.lower().replace(" ", "-"))
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `repr()` shows hidden characters such as spaces and `\n`, proving that `strip()` removed them.
- Each method returns a new string; `clean` itself does not change.
- `find` returns the index of the first match (or −1 when not found).

**Example 2**
- `split()` with no argument breaks the `df` line on any run of whitespace, producing 6 fields that we unpack into variables.
- `rstrip("%")` removes the percent sign from the right, so `int()` can convert it.
- `split(",")` then `strip()` on each piece cleans a messy comma-separated list.
- `" ".join(hosts)` builds a space-separated line.
- `lower().replace(" ", "-")` creates a slug suitable for a Kubernetes label.

## 7. Expected Output

**Example 1:**

```text
'   Production-Server  \n'
'Production-Server'
production-server
PRODUCTION-SERVER
Production-DB
True False
Position of '-': 10
Count of 'o': 2
True False
```

**Example 2:**

```text
Fields: ['/dev/sda1', '50G', '41G', '9.0G', '82%', '/']
Mount / is 82% full
Warning: high disk usage on /dev/sda1
Hosts: ['web-01', 'web-02', 'web-03']
Ansible inventory line: web-01 web-02 web-03
Confirmed? True
Label: payment-service-api
```

## 8. Common Mistakes

**1. Expecting methods to change the original**

`name.upper()` alone does nothing visible. Use `name = name.upper()`.

**2. Wrong `join` order**

`["a", "b"].join(",")` is an error. It is `",".join(["a", "b"])`.

**3. `split(" ")` on irregular spacing**

`"a  b".split(" ")` gives `['a', '', 'b']`. Use `split()` with no argument for whitespace.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Clean user input:** Given `env = "  StAgInG \n"`, produce `staging` and print whether it is one of dev/staging/prod.
- **Task 2 (Medium) — Parse key=value:** Given the line `"DB_HOST=db.internal; DB_PORT=5432; DB_NAME=orders"`, split it into pairs and print each key and value on its own line, e.g. `DB_HOST -> db.internal`.
- **Task 3 (Practical Challenge) — Process listing parser:** Given a line of `ps aux` output `"www-data  1234  12.5  3.1  456789  65432 ?  S  10:01  0:42 nginx: worker process"`, extract the user, PID, CPU %, memory % and the command (everything from the 11th field). Print a summary and flag the process if CPU > 10.

## 10. DevOps/MLOps Connection

- **DevOps:** parsing `df`, `ps`, `kubectl get pods` output; cleaning environment variables; building labels and tags.
- **Cloud:** splitting ARNs (`arn.split(":")`) to get account ID, region and resource.
- **Data engineering:** cleaning messy text columns (strip, lower, replace) before loading.
- **ML:** text pre-processing — lower-casing and tokenising (`split`) is the first step of every NLP pipeline.

## 11. Interview Questions

**Q1. What is the difference between `strip()`, `lstrip()` and `rstrip()`?**

<details><summary>Show answer</summary>

`strip` removes characters from both ends, `lstrip` from the left only, `rstrip` from the right only.

</details>

**Q2. How do you split a string into a list and join it back?**

<details><summary>Show answer</summary>

`parts = s.split(sep)` and `sep.join(parts)`.

</details>

**Q3. What does `find()` return when the substring is missing, and how is `index()` different?**

<details><summary>Show answer</summary>

`find` returns −1; `index` raises `ValueError`.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 19 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 018](../../02-strings-collections/day-018/README.md) | [📚 Phase 2: Strings and Collections](../README.md) | [🏠 Home](../../README.md) | [Day 020 ➡](../../02-strings-collections/day-020/README.md)
