# Day 047 — Reading Files

[⬅ Day 046](../../05-files-exceptions/day-046/README.md) | [📚 Phase 5: File Handling and Error Handling](../README.md) | [🏠 Home](../../README.md) | [Day 048 ➡](../../05-files-exceptions/day-048/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 5 — File Handling and Error Handling | 🟡 Intermediate | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Read a whole file with `read()`
- Read line by line with a loop, `readline()` and `readlines()`
- Process large files memory-efficiently

## 2. Topic Explanation

There are several ways to read a text file:

| Method | Returns | Use when |
|---|---|---|
| `file.read()` | whole file as one string | small files |
| `file.readline()` | the next line | reading a header first |
| `file.readlines()` | list of all lines | small files you need as a list |
| `for line in file:` | one line at a time | **large files (best)** |

Looping directly over the file object is **memory-efficient**: Python keeps only one line in memory, so you can process a 20 GB log file on a small machine. That's how `grep` and `awk` work too.

Each line keeps its trailing newline `\n`; use `line.strip()` or `line.rstrip("\n")`.

`file.read().splitlines()` gives a list of lines without the newline characters.

> Run the examples from inside this day's folder (`cd` into it first) so the relative file paths work.

## 3. Syntax

```python
with open(path, encoding="utf-8") as f:
    text = f.read()            # everything
    first = f.readline()       # one line
    lines = f.readlines()      # list of lines

with open(path, encoding="utf-8") as f:
    for line in f:             # streaming, memory-efficient
        process(line.strip())
```

| Part | Meaning |
|---|---|
| `read()` | Entire content as a string. |
| `readline()` | Next line including `\n`; empty string at end of file. |
| `readlines()` | List of all lines. |
| `for line in f` | Iterates lazily, line by line. |

## 4. Example 1 — Basic Example: Different ways to read

```python
with open("requirements_sample.txt", encoding="utf-8") as f:
    whole = f.read()
print("read() ->", len(whole), "characters")

with open("requirements_sample.txt", encoding="utf-8") as f:
    first_line = f.readline()
    second_line = f.readline()
print("readline() ->", repr(first_line), repr(second_line))

with open("requirements_sample.txt", encoding="utf-8") as f:
    lines = f.readlines()
print("readlines() ->", len(lines), "lines")

packages = []
with open("requirements_sample.txt", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        name, version = line.split("==")
        packages.append((name, version))
print("Pinned packages:", packages)
```

## 5. Example 2 — Practical Example: Analysing an nginx access log line by line

```python
status_counts = {}
bytes_total = 0
ip_hits = {}
errors = []

with open("nginx_access.log", encoding="utf-8") as log_file:
    for line_number, line in enumerate(log_file, start=1):
        parts = line.split()
        ip = parts[0]
        method = parts[4].strip('"')
        path = parts[5]
        status = int(parts[7])
        size = int(parts[8])

        status_counts[status] = status_counts.get(status, 0) + 1
        ip_hits[ip] = ip_hits.get(ip, 0) + 1
        bytes_total += size
        if status >= 400:
            errors.append(f"line {line_number}: {status} {method} {path} from {ip}")

print("Requests by status:", dict(sorted(status_counts.items())))
print("Total bytes served:", bytes_total)
top_ip = max(ip_hits, key=ip_hits.get)
print(f"Top client: {top_ip} ({ip_hits[top_ip]} requests)")
print("Errors:")
for e in errors:
    print("  ", e)
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `read()` returns one big string; `readline()` returns one line at a time (note the `\n` shown by `repr`).
- `readlines()` returns a list.
- The final loop is the real-world pattern: stream lines, skip blanks/comments, parse the rest.

**Example 2**
- Each log line is split on whitespace; fixed positions give IP, method, path, status and size.
- Counters are dicts (Day 27); errors (status ≥ 400) are collected with their line numbers.
- Because we loop over the file object, this works for a log of any size.

## 7. Expected Output

**Example 1:**

```text
read() -> 99 characters
readline() -> '# production dependencies\n' 'requests==2.32.3\n'
readlines() -> 7 lines
Pinned packages: [('requests', '2.32.3'), ('pyyaml', '6.0.2'), ('fastapi', '0.115.0'), ('pytest', '8.3.3')]
```

**Example 2:**

```text
Requests by status: {200: 3, 401: 1, 404: 1, 500: 1}
Total bytes served: 2496
Top client: 192.168.1.10 (2 requests)
Errors:
   line 3: 401 POST /api/login from 10.0.0.5
   line 4: 404 GET /missing from 192.168.1.10
   line 5: 500 GET /api/orders from 10.0.0.9
```

## 8. Common Mistakes

**1. `read()` on huge files**

Loading a multi-GB file with `read()` can exhaust memory. Iterate line by line.

**2. Forgetting the newline**

`line == "web-01"` is False when line is `"web-01\n"`. Strip first.

**3. Reading twice from the same object**

After `read()`, the file position is at the end; a second `read()` returns `""`. Re-open or use `f.seek(0)`.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Count lines and words:** Read `nginx_access.log` and print the number of lines, words and characters (like `wc`).
- **Task 2 (Medium) — Find unique IPs:** Read `nginx_access.log` and print the sorted set of unique client IPs and how many there are.
- **Task 3 (Practical Challenge) — Endpoint report:** From `nginx_access.log`, compute for each path: number of requests and number of errors (status ≥ 400). Print a table sorted by requests (descending) and the overall error rate.

## 10. DevOps/MLOps Connection

- **DevOps:** log analysis, parsing `requirements.txt`, reading inventory files, scanning config files for secrets.
- **Cloud:** reading CloudTrail/ALB logs downloaded from S3.
- **Data engineering:** streaming line-by-line is how you process data bigger than memory.
- **ML:** reading text corpora or label files for training.

## 11. Interview Questions

**Q1. How do you read a large file without loading it into memory?**

<details><summary>Show answer</summary>

Iterate over the file object (`for line in f:`), which reads one line at a time.

</details>

**Q2. What does `readline()` return at the end of a file?**

<details><summary>Show answer</summary>

An empty string `''`.

</details>

**Q3. How do you remove the trailing newline from each line?**

<details><summary>Show answer</summary>

`line.rstrip('\n')` or `line.strip()` (which also removes other whitespace).

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 47 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 046](../../05-files-exceptions/day-046/README.md) | [📚 Phase 5: File Handling and Error Handling](../README.md) | [🏠 Home](../../README.md) | [Day 048 ➡](../../05-files-exceptions/day-048/README.md)
