# Day 072 — Regular Expressions

[⬅ Day 071](../../07-devops-automation/day-071/README.md) | [📚 Phase 7: Python for DevOps Automation](../README.md) | [🏠 Home](../../README.md) | [Day 073 ➡](../../07-devops-automation/day-073/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 7 — Python for DevOps Automation | 🟠 Intermediate+ | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Write regex patterns with character classes, quantifiers, anchors and groups
- Use `re.search`, `re.findall`, `re.finditer`, `re.sub` and `re.compile`
- Extract structured data (IPs, timestamps, status codes) from text

## 2. Topic Explanation

A **regular expression (regex)** is a mini-language for describing text patterns. You've used them with `grep -E`, `sed` and `awk`; Python's `re` module uses the same ideas.

| Pattern | Matches |
|---|---|
| `\d` / `\D` | a digit / non-digit |
| `\w` | letter, digit or `_` |
| `\s` | whitespace |
| `.` | any character (except newline) |
| `[abc]`, `[a-z0-9]` | one of the listed characters |
| `^` / `$` | start / end of the string (or line with `re.M`) |
| `*` `+` `?` | 0+, 1+, 0 or 1 times |
| `{3}` / `{1,3}` | exactly 3 / between 1 and 3 times |
| `( )` | capturing group |
| `(?P<name> )` | named group |
| `\|` | OR |
| `\.` | a literal dot (escape special characters) |

Always write patterns as **raw strings** `r"\d+"` so backslashes reach the regex engine untouched (Day 4!).

Functions:
- `re.search(p, s)` — first match anywhere (or `None`).
- `re.match(p, s)` — match only at the start.
- `re.findall(p, s)` — list of all matches (or of groups).
- `re.finditer(p, s)` — iterator of match objects.
- `re.sub(p, repl, s)` — search and replace.
- `re.compile(p)` — pre-compile a pattern you use many times.

Tip: test patterns at regex101.com (choose the Python flavour).

## 3. Syntax

```python
import re
m = re.search(r"(?P<code>\d{3})", text)
if m:
    m.group("code"), m.group(0), m.groups()
re.findall(r"\d+", text)
re.sub(r"password=\S+", "password=****", text)
pattern = re.compile(r"ERROR\s+(.*)", re.IGNORECASE)
```

| Part | Meaning |
|---|---|
| `r"..."` | Raw string — always use for regex. |
| `search vs match` | `search` anywhere; `match` only at the beginning. |
| `groups` | `( )` capture parts; `(?P<name>...)` captures by name. |
| `flags` | `re.IGNORECASE`, `re.MULTILINE`, `re.VERBOSE`. |

## 4. Example 1 — Basic Example: Regex fundamentals

```python
import re

text = "Order 1042 shipped to 10.0.3.25 on 2026-11-20; order 1043 pending. Contact ops@example.com"

print("First number :", re.search(r"\d+", text).group())
print("All numbers  :", re.findall(r"\d+", text))
print("Dates        :", re.findall(r"\d{4}-\d{2}-\d{2}", text))
print("IPv4         :", re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", text))
print("Email        :", re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", text).group())

m = re.search(r"order (?P<id>\d+) (?P<state>\w+)", text, re.IGNORECASE)
print("Named groups :", m.group("id"), m.group("state"), m.groupdict())

print("Starts with 'Order'?", bool(re.match(r"Order", text)))
print("Masked       :", re.sub(r"\d{4}-\d{2}-\d{2}", "<DATE>", text)[:60])
```

## 5. Example 2 — Practical Example: Parsing an access log and masking secrets

```python
import re

ACCESS_LOG = """\
192.168.1.10 - - [20/Nov/2026:10:00:01 +0000] "GET /index.html HTTP/1.1" 200 512 "-" "curl/8.5"
10.0.0.5 - - [20/Nov/2026:10:00:04 +0000] "POST /api/login HTTP/1.1" 401 64 "-" "Mozilla/5.0"
10.0.0.9 - - [20/Nov/2026:10:00:09 +0000] "GET /api/orders?id=7 HTTP/1.1" 500 256 "-" "python-requests/2.32"
bad line without the right format
"""

LINE = re.compile(r"""
    ^(?P<ip>\d{1,3}(?:\.\d{1,3}){3})         # client IP
    \s-\s-\s
    \[(?P<time>[^\]]+)\]\s                    # [timestamp]
    "(?P<method>[A-Z]+)\s(?P<path>\S+)\s[^"]+"\s
    (?P<status>\d{3})\s(?P<size>\d+)          # status and size
""", re.VERBOSE)

for line in ACCESS_LOG.splitlines():
    m = LINE.match(line)
    if not m:
        print("SKIP:", line)
        continue
    d = m.groupdict()
    print(f"{d['ip']:<13} {d['method']:<5} {d['path']:<16} {d['status']} {d['size']:>4}B @ {d['time']}")

config_dump = "db_host=10.0.0.20 db_password=Sup3rS3cret api_token=ghp_abc123XYZ debug=true"
masked = re.sub(r"(?i)(password|token|secret)=\S+", r"\1=****", config_dump)
print("Masked config:", masked)

versions = ["v1.2.3", "1.10.0", "v2.0.0-rc.1", "release-7", "v3.1"]
semver = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)(?:-([\w.]+))?$")
for v in versions:
    m = semver.match(v)
    print(f"{v:<12} ->", m.groups() if m else "not semver")
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `\d+` = one or more digits; `\d{4}-\d{2}-\d{2}` = a date.
- The IP pattern `(?:\d{1,3}\.){3}\d{1,3}` repeats "1–3 digits and a dot" three times; `(?:...)` is a non-capturing group so `findall` returns whole matches. `\b` marks word boundaries.
- Named groups make results readable via `groupdict()`.
- `re.match` only checks the start of the string.

**Example 2**
- `re.VERBOSE` lets us split a complex pattern over several lines with comments.
- `LINE.match(line)` returns `None` for the malformed line, which we skip.
- `re.sub` with a group reference `\1` keeps the key name and replaces only the secret value; `(?i)` makes it case-insensitive.
- The semantic-version pattern uses anchors `^...$` so `v3.1` (missing patch) doesn't match.

## 7. Expected Output

**Example 1:**

```text
First number : 1042
All numbers  : ['1042', '10', '0', '3', '25', '2026', '11', '20', '1043']
Dates        : ['2026-11-20']
IPv4         : ['10.0.3.25']
Email        : ops@example.com
Named groups : 1042 shipped {'id': '1042', 'state': 'shipped'}
Starts with 'Order'? True
Masked       : Order 1042 shipped to 10.0.3.25 on <DATE>; order 1043 pendin
```

**Example 2:**

```text
192.168.1.10  GET   /index.html      200  512B @ 20/Nov/2026:10:00:01 +0000
10.0.0.5      POST  /api/login       401   64B @ 20/Nov/2026:10:00:04 +0000
10.0.0.9      GET   /api/orders?id=7 500  256B @ 20/Nov/2026:10:00:09 +0000
SKIP: bad line without the right format
Masked config: db_host=10.0.0.20 db_password=**** api_token=**** debug=true
v1.2.3       -> ('1', '2', '3', None)
1.10.0       -> ('1', '10', '0', None)
v2.0.0-rc.1  -> ('2', '0', '0', 'rc.1')
release-7    -> not semver
v3.1         -> not semver
```

## 8. Common Mistakes

**1. Forgetting raw strings**

`"\d"` happens to work but `"\b"` is a backspace character! Always use `r"..."`.

**2. Greedy `.*`**

`<.*>` on `<a><b>` matches the whole string. Use the non-greedy `.*?` or a negated class `[^>]*`.

**3. Regex for everything**

For JSON use `json`, for CSV use `csv`, for simple checks use `in`/`startswith`. Regex is for semi-structured text.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Find all hashtags:** Extract all hashtags from `"Learning #Python for #DevOps and #MLOps #100DaysOfCode"`.
- **Task 2 (Medium) — Validate hostnames:** Write `is_valid_hostname(name)` that accepts lowercase names like `web-01` or `db-prod-3` (letters, digits, hyphens, 3–20 chars, not starting/ending with a hyphen). Test 5 names.
- **Task 3 (Practical Challenge) — Kubernetes event parser:** Parse these event lines with one compiled regex into dicts (age, type, reason, object, message): `5m Warning BackOff pod/api-7d9f Back-off restarting failed container`, `2m Normal Pulled pod/api-7d9f Successfully pulled image`, `30s Warning FailedScheduling pod/worker-1 0/3 nodes are available`. Print only Warning events and count reasons.

## 10. DevOps/MLOps Connection

- **DevOps:** log parsing (nginx, syslog, application logs), extracting versions/tags, validating names in CI, masking secrets before printing logs.
- **Cloud:** parsing ARNs, validating resource names against naming conventions, extracting values from CLI output.
- **Data/ML:** cleaning text, extracting features from log lines (status, latency) to build datasets for anomaly-detection models.

## 11. Interview Questions

**Q1. What is the difference between `re.search` and `re.match`?**

<details><summary>Show answer</summary>

`match` only matches at the beginning of the string; `search` scans the whole string for the first match.

</details>

**Q2. Why use raw strings for regex patterns?**

<details><summary>Show answer</summary>

So Python doesn't interpret backslash escapes before the regex engine sees them.

</details>

**Q3. What does `.*?` mean?**

<details><summary>Show answer</summary>

Non-greedy 'any characters': match as few characters as possible.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 72 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 071](../../07-devops-automation/day-071/README.md) | [📚 Phase 7: Python for DevOps Automation](../README.md) | [🏠 Home](../../README.md) | [Day 073 ➡](../../07-devops-automation/day-073/README.md)
